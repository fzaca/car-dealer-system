import os

MINIO_PUBLIC_HOST = os.getenv('MINIO_PUBLIC_HOST', 'localhost')
MINIO_PUBLIC_PORT = os.getenv('MINIO_PUBLIC_PORT', '9000')
MINIO_PUBLIC_URL = f"{MINIO_PUBLIC_HOST}:{MINIO_PUBLIC_PORT}"

MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin123')

MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'assets')
