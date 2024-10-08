from django.conf import settings
from minio import Minio

from resources.constants import MINIO_ACCESS_KEY, MINIO_SECRET_KEY
from resources.constants import MINIO_PUBLIC_URL, MINIO_BUCKET
from resources.constants import MINIO_PUBLIC_HOST


def get_minio_client():
    use_ssl = MINIO_PUBLIC_URL.startswith('https')

    client = Minio(
        MINIO_PUBLIC_URL.replace('http://', '').replace('https://', ''),
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=use_ssl
    )
    return client


def generate_public_url(file_name):
    if settings.ENV == "local":
        return f"http://{MINIO_PUBLIC_URL}/{MINIO_BUCKET}/{file_name}"
    else:
        return f"{MINIO_PUBLIC_HOST}/{MINIO_BUCKET}/{file_name}"
