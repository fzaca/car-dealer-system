import os
import sys
from decouple import config

from django.core.management import execute_from_command_line


def main():
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings.local")
	os.environ.setdefault("ENV", config("ENV", default="local"))
	try:
		execute_from_command_line(sys.argv)
	except ImportError as exc:
		raise ImportError(
			"Couldn't import Django. Are you sure it's installed and "
			"available on your PYTHONPATH environment variable? Did you "
			"forget to activate a virtual environment?"
		) from exc


if __name__ == "__main__":
	main()
