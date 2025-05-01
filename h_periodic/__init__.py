import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from h_periodic._version import get_version

sentry_sdk.init(
    integrations=[CeleryIntegration()],
    # Enable Sentry's "Releases" feature, see:
    # https://docs.sentry.io/platforms/python/configuration/options/#release
    release=get_version(),
)
