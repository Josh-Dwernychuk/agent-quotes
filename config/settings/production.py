from .base import * # noqa

# Security Checks - recommendations from ./manage.py check --deploy #
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Redirect to https:
SECURE_SSL_REDIRECT = True
