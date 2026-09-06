from .settings import *

# Keep automated checks independent of the configured remote database.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
