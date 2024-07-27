import json
import os
import tarfile
import mimetypes

from django.conf import settings
from django.core.management.base import BaseCommand
import gdown
from minio.error import S3Error

from resources.constants import MINIO_BUCKET, MINIO_PUBLIC_HOST, MINIO_PUBLIC_URL
from resources.utils.minio_utils import get_minio_client

FILE_URL = "https://drive.google.com/file/d/1xkj7Wg5pc1I14t_EzohxivXxTw9_T0th/view?usp=sharing"
DEST_FOLDER = "resources/data"
CAR_IMAGES_FOLDER = os.path.join(DEST_FOLDER, "car_images")


class Command(BaseCommand):
    help = "Download and load car images"

    def handle(self, *args, **kwargs):
        if not os.path.exists(CAR_IMAGES_FOLDER):
            self.download_and_extract_images(FILE_URL, DEST_FOLDER)
            self.stdout.write(self.style.SUCCESS("Successfully downloaded and extracted the tar.gz file"))
        else:
            self.stdout.write(self.style.SUCCESS("Car images folder already exists. Skipping download."))

        self.client = get_minio_client()
        self.setup_bucket(MINIO_BUCKET)
        self.upload_images(CAR_IMAGES_FOLDER)

    def setup_bucket(self, bucket_name):
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:GetBucketLocation",
                        "s3:ListBucket"
                    ],
                    "Resource": f"arn:aws:s3:::{bucket_name}"
                },
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        policy_json = json.dumps(policy)
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                self.stdout.write(self.style.SUCCESS(f"Bucket '{bucket_name}' created."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Bucket '{bucket_name}' already exists."))
            self.client.set_bucket_policy(bucket_name, policy_json)
        except S3Error as err:
            self.stdout.write(self.style.ERROR(f"Error occurred: {err}"))

    def upload_images(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                if not file.endswith("image_0.jpg"):
                    continue
                file_path = os.path.join(root, file)
                object_name = os.path.relpath(file_path, folder_path)
                content_type, _ = mimetypes.guess_type(file_path)
                try:
                    self.client.fput_object(
                        MINIO_BUCKET,
                        object_name,
                        file_path,
                        content_type=content_type
                    )
                    if settings.ENV == "local":
                        public_url = f"{MINIO_PUBLIC_URL}/{MINIO_BUCKET}/{object_name}"
                    else:
                        public_url = f"{MINIO_PUBLIC_HOST}/{MINIO_BUCKET}/{object_name}"
                    self.stdout.write(self.style.SUCCESS(f"File '{file}' uploaded successfully.\nPublic URL: {public_url}"))
                except S3Error as err:
                    self.stdout.write(self.style.ERROR(f"Error uploading '{file}': {err}"))

    @staticmethod
    def download_and_extract_images(drive_url, dest_folder):
        file_id = drive_url.split('/d/')[1].split('/view')[0]
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        tar_gz_filename = "downloaded_file.tar.gz"

        gdown.download(download_url, tar_gz_filename, quiet=False)

        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        with tarfile.open(tar_gz_filename, "r:gz") as tar:
            tar.extractall(path=dest_folder)

        os.remove(tar_gz_filename)
