import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(integrations=[CeleryIntegration()])
