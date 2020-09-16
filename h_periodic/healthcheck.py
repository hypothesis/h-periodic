import os

import kombu
from pyramid.config import Configurator
from pyramid.view import exception_view_config, view_config, view_defaults


@view_defaults(route_name="status", renderer="json", request_method="GET")
class StatusViews:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @staticmethod
    @view_config()
    def status():
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


def create_app(_global_config, **settings):
    with Configurator(settings=settings) as config:
        config.add_route("status", "/_status")
        config.scan()

    return config.make_wsgi_app()
