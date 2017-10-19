#!/usr/bin/env python3
import os
import sys

# if we're not in ~~the matrix~~ docker, go ahead and drop us into docker.
if not os.path.exists("/.dockerenv"):
    os.system("docker-compose exec auth_gateway " + ' '.join(sys.argv))
    sys.exit()
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_gateway.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
