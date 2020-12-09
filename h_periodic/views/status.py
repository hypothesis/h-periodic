import os
from os import environ

import kombu
import psutil
from kombu.exceptions import KombuError
from pyramid.view import view_config


class StatusView:
    H_PID_FILE = "h-celerybeat.pid"
    H_BROKER_VAR = "H_BROKER_URL"
    CHECKMATE_PID_FILE = "checkmate-celerybeat.pid"
    CHECKMATE_BROKER_VAR = "CHECKMATE_BROKER_URL"

    def __init__(self, _context, request):
        self.request = request

    @view_config(route_name="status", renderer="json", request_method="GET")
    def status(self):
        data = {
            "h": self._get_status(self.H_PID_FILE, self.H_BROKER_VAR),
            "checkmate": self._get_status(
                self.CHECKMATE_PID_FILE, self.CHECKMATE_BROKER_VAR
            ),
        }

        h_ok = data["h"]["status"] == "ok"
        checkmate_ok = data["checkmate"]["status"] == "ok"

        if h_ok and checkmate_ok:
            status_code, status = 200, "ok"
        elif not h_ok and not checkmate_ok:
            status_code, status = 500, "down"
        else:
            status_code, status = 200, "degraded"

        data["status"] = status
        self.request.response.status_int = status_code

        return data

    @classmethod
    def _get_status(cls, pid_file, broker_var):
        pid_ok = cls._check_pid_file(pid_file)
        connection_ok = cls._check_broker(broker_var)

        return {
            "beat": cls._summarise(pid_ok),
            "connection": cls._summarise(connection_ok),
            "status": cls._summarise(pid_ok, connection_ok),
        }

    @classmethod
    def _check_pid_file(cls, pid_file):
        if not os.path.exists(pid_file):
            return False

        return psutil.pid_exists(int(open(pid_file, "r").read()))

    @classmethod
    def _check_broker(cls, broker_var):
        broker_url = environ.get(broker_var)

        if broker_url:
            connection = kombu.Connection(broker_url)

            try:
                connection.connect()
                return True
            except (KombuError, ConnectionRefusedError):
                pass
            finally:
                connection.close()

        return False

    @staticmethod
    def _summarise(*values):
        """Create a textual summary of a series of truthy values."""

        for value in values:
            if not value:
                return "down"

        return "ok"
