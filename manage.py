#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
from django.core.management import execute_from_command_line


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# 🔹 Force STATICFILES_STORAGE for collectstatic
if "collectstatic" in os.sys.argv:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello_world_project.settings")
    django.setup()
    from django.conf import settings
    settings.STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

execute_from_command_line(os.sys.argv)

if __name__ == '__main__':
    main()
