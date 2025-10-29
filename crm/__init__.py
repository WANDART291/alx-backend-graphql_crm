# crm/__init__.py
# Import the Celery app instance from the renamed file
from .celery_app import app as celery_app

__all__ = ('celery_app',)