from pyramid.config import Configurator


def create_app(_global_config, **settings):  # pragma: no cover
    with Configurator(settings=settings) as config:
        config.add_route("status", "/_status")
        config.scan("h_periodic.views")

    return config.make_wsgi_app()
