"""
WSGI config for agent-quotes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from django.core.wsgi import get_wsgi_application

# Using a Sentry wrapper to capture errors outside of the Django code
# More info here: https://docs.sentry.io/clients/python/integrations/django/
application = Sentry(get_wsgi_application())
