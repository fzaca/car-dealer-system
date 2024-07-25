import os
import sys
import environ

from django.core.management import execute_from_command_line


def main():
	env = os.getenv("ENV", "local")

	environ.Env.read_env(os.path.join(os.path.dirname(__file__), 'environments', f"{env}.env"))

	settings_module = f"service.settings.{env}"
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

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
