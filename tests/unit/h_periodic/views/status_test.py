import os
from unittest.mock import call, sentinel

import pytest
from h_matchers import Any
from kombu.exceptions import KombuError

from h_periodic.views.status import StatusView


class TestStatusView:
    @pytest.mark.usefixtures("with_everything_running")
    def test_it_with_everything_ok(self, pyramid_request, psutil, kombu):
        view = StatusView(sentinel.context, pyramid_request)
        result = view.status()

        assert psutil.pid_exists.call_args_list == [
            call(1234),  # Once for H
            call(4321),  # And once for Checkmate
        ]

        assert kombu.Connection.call_args_list == [
            call(sentinel.h_broker),
            call(sentinel.checkmate_broker),
        ]
        connection = kombu.Connection.return_value
        assert connection.connect.call_count == 2
        assert connection.close.call_count == 2

        assert result == {
            "h": {"beat": "ok", "connection": "ok", "status": "ok"},
            "checkmate": {"beat": "ok", "connection": "ok", "status": "ok"},
            "status": "ok",
        }
        assert view.request.response.status_int == 200

    @pytest.mark.usefixtures("with_everything_running")
    @pytest.mark.parametrize(
        "product,env_var",
        (
            ["h", StatusView.H_BROKER_VAR],
            ["checkmate", StatusView.CHECKMATE_BROKER_VAR],
        ),
    )
    def test_it_with_no_broker_url(self, pyramid_request, environ, product, env_var):
        environ[env_var] = None

        result = StatusView(sentinel.context, pyramid_request).status()

        assert result == Any.dict.containing(
            {
                product: Any.dict.containing({"connection": "down", "status": "down"}),
                "status": "degraded",
            }
        )

    @pytest.mark.usefixtures("with_everything_running")
    @pytest.mark.parametrize("exception", (KombuError, ConnectionRefusedError))
    def test_it_with_bad_broker_connection(
        self, pyramid_request, environ, kombu, exception
    ):
        environ[StatusView.H_BROKER_VAR] = sentinel.h_broker
        kombu.Connection.return_value.connect.side_effect = exception

        result = StatusView(sentinel.context, pyramid_request).status()

        assert result == {
            "h": Any.dict.containing({"connection": "down", "status": "down"}),
            "checkmate": Any.dict.containing({"connection": "down", "status": "down"}),
            "status": "down",
        }

    @pytest.mark.usefixtures("with_everything_running")
    @pytest.mark.parametrize(
        "product,pid_file",
        (("h", StatusView.H_PID_FILE), ("checkmate", StatusView.CHECKMATE_PID_FILE)),
    )
    def test_it_with_no_pid_file(self, pyramid_request, tmpdir, product, pid_file):
        os.unlink(tmpdir / pid_file)

        result = StatusView(sentinel.context, pyramid_request).status()

        assert result == Any.dict.containing(
            {
                product: Any.dict.containing({"beat": "down", "status": "down"}),
                "status": "degraded",
            }
        )

    @pytest.mark.usefixtures("with_everything_running")
    def test_it_with_pid_file_but_no_pid(self, pyramid_request, psutil):
        psutil.pid_exists.return_value = False

        result = StatusView(sentinel.context, pyramid_request).status()

        assert result == {
            "h": Any.dict.containing({"beat": "down", "status": "down"}),
            "checkmate": Any.dict.containing({"beat": "down", "status": "down"}),
            "status": "down",
        }

    @pytest.fixture
    def with_everything_running(self, environ, tmpdir):
        environ[StatusView.H_BROKER_VAR] = sentinel.h_broker
        environ[StatusView.CHECKMATE_BROKER_VAR] = sentinel.checkmate_broker

        h_pid_file = tmpdir / StatusView.H_PID_FILE
        h_pid_file.write("1234")

        checkmate_pid_file = tmpdir / StatusView.CHECKMATE_PID_FILE
        checkmate_pid_file.write("4321")

    @pytest.fixture
    def tmpdir(self, tmpdir):
        cwd = os.getcwd()

        try:  # pylint: disable=too-many-try-statements
            os.chdir(tmpdir)
            yield tmpdir
        finally:
            os.chdir(cwd)

    @pytest.fixture(autouse=True)
    def environ(self, patch):
        environ = patch("h_periodic.views.status.environ")

        # Make this dict like so multiple tests / fixtures can easily modify it
        # mock.patch.dict can't be used as a context manager until Python 3.8
        env_vars = {}
        environ.get = env_vars.get
        return env_vars

    @pytest.fixture(autouse=True)
    def psutil(self, patch):
        return patch("h_periodic.views.status.psutil")

    @pytest.fixture(autouse=True)
    def kombu(self, patch):
        return patch("h_periodic.views.status.kombu")
