import functools
from unittest import mock

import pytest
from pyramid import testing
from pyramid.request import Request


def autopatcher(request, target, **kwargs):
    """Patch and cleanup automatically. Wraps :py:func:`mock.patch`."""
    options = {"autospec": True}
    options.update(kwargs)
    patcher = mock.patch(target, **options)
    obj = patcher.start()
    request.addfinalizer(patcher.stop)
    return obj


@pytest.fixture
def patch(request):
    return functools.partial(autopatcher, request)


@pytest.fixture
def pyramid_config():
    with testing.testConfig(settings={}) as config:
        yield config


@pytest.fixture
def pyramid_request(pyramid_config):
    pyramid_request = Request.blank("/dummy")
    pyramid_request.registry = pyramid_config.registry

    return pyramid_request
