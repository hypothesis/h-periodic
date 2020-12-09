import os
from os import environ

import kombu
import psutil
from kombu.exceptions import KombuError
from pyramid.view import view_config


class StatusView:
    H_PID_FILE = "celerybeat.pid"
    H_BROKER_VAR = "BROKER_URL"

    def __init__(self, _context, request):
        self.request = request

    @view_config(route_name="status", renderer="json", request_method="GET")
    def status(self):
        data = {"h": self._get_status(self.H_PID_FILE, self.H_BROKER_VAR)}

        data["status"] = self._summarise(data["h"]["status"] == "ok")

        self.request.response.status_int = 200 if data["status"] == "ok" else 500

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
