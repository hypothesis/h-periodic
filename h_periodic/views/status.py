import os

import kombu
import psutil
from kombu.exceptions import KombuError
from pyramid.view import view_config, view_defaults


@view_defaults(route_name="status", renderer="json", request_method="GET")
class StatusView:
    H_PID_FILE = "celerybeat.pid"
    H_BROKER_VAR = "BROKER_URL"

    def __init__(self, _context, request):
        self.request = request

    @view_config()
    def status(self):
        data = {"h": self._get_status(self.H_PID_FILE, self.H_BROKER_VAR)}

        data["status"] = self._summarise(data["h"]["status"] == "ok")

        self.request.response.status_int = 200 if data["status"] == "ok" else 500

        return data

    @classmethod
    def _get_status(cls, pid_file, broker_var):
        if os.path.exists(pid_file):
            pid_ok = psutil.pid_exists(int(open(pid_file, "r").read()))
        else:
            pid_ok = False

        connection_ok = False
        broker_url = os.environ.get(broker_var)

        if broker_url:
            connection = kombu.Connection(broker_url)

            try:
                connection.connect()
                connection_ok = True
            except KombuError:
                pass
            finally:
                connection.close()

        return {
            "beat": cls._summarise(pid_ok),
            "connection": cls._summarise(connection_ok),
            "status": cls._summarise(pid_ok, connection_ok),
        }

    @staticmethod
    def _summarise(*values):
        """Create a textual summary of a series of truthy values."""

        for value in values:
            if not value:
                return "down"

        return "ok"
