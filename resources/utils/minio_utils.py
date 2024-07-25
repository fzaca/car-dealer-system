from minio import Minio

from resources.constants import MINIO_ACCESS_KEY, MINIO_SECRET_KEY
from resources.constants import MINIO_URL


def get_minio_client():
    use_ssl = MINIO_URL.startswith('https')

    client = Minio(
        MINIO_URL.replace('http://', '').replace('https://', ''),
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=use_ssl
    )
    return client
