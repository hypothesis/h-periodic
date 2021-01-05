import functools
from unittest import mock

import pytest


def autopatcher(request, target, **kwargs):  # pragma: no cover
    """Patch and cleanup automatically. Wraps :py:func:`mock.patch`."""
    options = {"autospec": True}
    options.update(kwargs)
    patcher = mock.patch(target, **options)
    obj = patcher.start()
    request.addfinalizer(patcher.stop)
    return obj


@pytest.fixture
def patch(request):  # pragma: no cover
    return functools.partial(autopatcher, request)
