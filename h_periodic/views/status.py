import os

import kombu
import psutil
from pyramid.view import exception_view_config, view_config, view_defaults


@view_defaults(route_name="status", renderer="json", request_method="GET")
class StatusViews:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @staticmethod
    @view_config()
    def status():
        # First check that the `celery beat` process is running.
        if not psutil.pid_exists(int(open("celerybeat.pid", "r").read())):
            raise RuntimeError("It looks like `celery beat` isn't running")

        # Next check that we can connect to the message broker at BROKER_URL.
        connection = kombu.Connection(os.environ["BROKER_URL"])
        try:
            connection.connect()
        finally:
            connection.close()

        return {"status": "ok"}

    @exception_view_config(Exception)
    def status_exception(self):
        self.request.response.status_int = 500
        return {"status": "error", "reason": repr(self.context)}
