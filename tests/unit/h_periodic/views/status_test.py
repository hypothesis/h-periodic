import os
from unittest.mock import sentinel

import pytest
from h_matchers import Any
from kombu.exceptions import KombuError

from h_periodic.views.status import StatusView


class TestStatusView:
    # pylint: disable=too-many-arguments
    def test_it_with_everything_ok(
        self, tmpdir, pyramid_request, environ, psutil, kombu
    ):
        environ[StatusView.H_BROKER_VAR] = sentinel.h_broker

        h_pid_file = tmpdir / StatusView.H_PID_FILE
        h_pid_file.write("1234")

        view = StatusView(sentinel.context, pyramid_request)
        result = view.status()

        psutil.pid_exists.assert_called_once_with(1234)

        kombu.Connection.assert_called_once_with(sentinel.h_broker)
        connection = kombu.Connection.return_value
        connection.connect.assert_called_once_with()
        connection.close.assert_called_once_with()

        assert result == {
            "h": {"beat": "ok", "connection": "ok", "status": "ok"},
            "status": "ok",
        }
        assert view.request.response.status_int == 200

    def test_it_with_no_broker_url(self, pyramid_request, environ):
        environ[StatusView.H_BROKER_VAR] = None

        result = StatusView(sentinel.context, pyramid_request).status()

        assert result == {
            "h": Any.dict.containing({"connection": "down", "status": "down"}),
            "status": "down",
        }

    @pytest.mark.parametrize("exception", (KombuError, ConnectionRefusedError))
    def test_it_with_bad_broker_connection(
        self, pyramid_request, environ, kombu, exception
    ):
        environ[StatusView.H_BROKER_VAR] = sentinel.h_broker
        kombu.Connection.return_value.connect.side_effect = exception

        result = StatusView(sentinel.context, pyramid_request).status()

        assert result == {
            "h": Any.dict.containing({"connection": "down", "status": "down"}),
            "status": "down",
        }

    def test_it_with_no_pid_file(self, pyramid_request, tmpdir):
        result = StatusView(sentinel.context, pyramid_request).status()

        assert result == {
            "h": Any.dict.containing({"beat": "down", "status": "down"}),
            "status": "down",
        }

    def test_it_with_pid_file_but_no_pid(self, pyramid_request, tmpdir, psutil):
        h_pid_file = tmpdir / StatusView.H_PID_FILE
        h_pid_file.write("1234")
        psutil.pid_exists.return_value = False

        result = StatusView(sentinel.context, pyramid_request).status()

        assert result == {
            "h": Any.dict.containing({"beat": "down", "status": "down"}),
            "status": "down",
        }

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
