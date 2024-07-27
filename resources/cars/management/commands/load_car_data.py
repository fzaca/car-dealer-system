import csv
import logging
import os
import re

import requests
from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand
from tqdm import tqdm

from resources.cars.models import Brand, CarModel, Car
from resources.constants import MINIO_BUCKET, MINIO_PUBLIC_HOST, MINIO_PUBLIC_URL


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Download and load car data'

    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data')

    if settings.ENV == "local":
        BASE_IMAGE_URL = f"http://{MINIO_PUBLIC_URL}/{MINIO_BUCKET}"
    else:
        BASE_IMAGE_URL = f"{MINIO_PUBLIC_HOST}/{MINIO_BUCKET}"

    FILES = {
        'Basic_table.csv': 'https://drive.google.com/uc?export=download&id=1hSuOBapbya9WznMDdT6hkgQ30DPUs9AT',
        'Ad_table.csv': 'https://drive.google.com/uc?export=download&id=1zRtkRRSM0ixap3JDpedaRxcPQlwBrlUp',
        'Image_table.csv': 'https://drive.google.com/uc?export=download&id=1oYzGYllZCt8O2Q-yCn1rY5Lqn8zvxi3p',
        'Price_table.csv': 'https://drive.google.com/uc?export=download&id=1BL9iaIHFF8U8mSKccQ6NtxU9ey_ie1_X',
        'Sales_table.csv': 'https://drive.google.com/uc?export=download&id=110VDa5Pc9oPI2EPB3GE1yuYF9HgHmEwP',
        'Trim_table.csv': 'https://drive.google.com/uc?export=download&id=1DKWOkhxKq58lyGpQOmOzWQ1CBszbmtgx',
    }

    def handle(self, *args, **kwargs):
        os.makedirs(self.BASE_DIR, exist_ok=True)
        self.download_files()
        self.load_brands()
        self.load_car_models()
        self.load_cars()
        self.stdout.write(self.style.SUCCESS('Successfully loaded car data'))

    def download_files(self):
        for file_name, url in self.FILES.items():
            file_path = os.path.join(self.BASE_DIR, file_name)
            if not os.path.exists(file_path):
                try:
                    self.stdout.write(f'Downloading {file_name}...')
                    response = requests.get(url)
                    response.raise_for_status()
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    self.stdout.write(f'Successfully downloaded {file_name}')
                except requests.exceptions.RequestException as e:
                    logger.error(f'Failed to download {file_name}: {e}')
                    self.stdout.write(self.style.ERROR(f'Failed to download {file_name}'))
                except Exception as e:
                    logger.error(f'An error occurred while downloading {file_name}: {e}')
                    self.stdout.write(self.style.ERROR(f'An error occurred while downloading {file_name}'))

    def load_brands(self):
        try:
            self.stdout.write("Dropping existing brands...")
            Brand.objects.all().delete()

            brands = []
            with open(os.path.join(self.BASE_DIR, 'Basic_table.csv'), newline='', encoding='utf-8') as csvfile:
                reader = list(csv.DictReader(csvfile))
                brand_names = {row['Automaker'] for row in reader}
                for name in brand_names:
                    brands.append(Brand(name=name))

            Brand.objects.bulk_create(brands)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(brands)} brands'))
            logger.info('Successfully loaded brands')
        except Exception as e:
            logger.error(f'An error occurred while loading brands: {e}')
            self.stdout.write(self.style.ERROR('An error occurred while loading brands'))

    def load_car_models(self):
        try:
            self.stdout.write("Dropping existing car models...")
            CarModel.objects.all().delete()

            car_models = []
            brands = {brand.name: brand for brand in Brand.objects.all()}
            with open(os.path.join(self.BASE_DIR, 'Basic_table.csv'), newline='', encoding='utf-8') as csvfile:
                reader = list(csv.DictReader(csvfile))
                for row in reader:
                    brand = brands.get(row['Automaker'])
                    if brand:
                        car_models.append(CarModel(name=row['Genmodel'], brand=brand))

            CarModel.objects.bulk_create(car_models)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(car_models)} car models'))
            logger.info('Successfully loaded car models')
        except Exception as e:
            logger.error(f'An error occurred while loading car models: {e}')
            self.stdout.write(self.style.ERROR('An error occurred while loading car models'))

    def load_cars(self):
        try:
            self.stdout.write("Dropping existing cars...")
            Car.objects.all().delete()

            brands = {brand.name: brand for brand in Brand.objects.all()}
            car_models = {(model.brand.name, model.name): model for model in CarModel.objects.select_related('brand').all()}

            cars_to_create = []
            with open(os.path.join(self.BASE_DIR, 'Ad_table.csv'), newline='', encoding='utf-8') as csvfile:
                reader = list(csv.DictReader(csvfile))
                for row in tqdm(reader, desc="Preparing cars"):
                    car = self.prepare_car(row.copy(), brands, car_models)
                    if car:
                        cars_to_create.append(car)

            self.bulk_create_cars(cars_to_create)
        except Exception as e:
            logger.error(f'An error occurred while loading cars: {e}')
            self.stdout.write(self.style.ERROR('An error occurred while loading cars'))

    def prepare_car(self, row, brands, car_models):
        brand = brands.get(row['Maker'])
        car_model = car_models.get((row['Maker'], row[' Genmodel']))

        if not brand or not car_model:
            return None

        try:
            engine_size = float(row['Engin_size'].replace('L', '').strip() or 0)
        except ValueError:
            engine_size = 0.0

        try:
            price = float(row['Price'] or 0)
        except ValueError:
            price = 0.0

        year = int(row['Reg_year'] or 0)
        mileage = int(re.sub(r'[^\d]', '', row['Runned_Miles']) or 0)
        seats = int(row['Seat_num'] or 0)
        doors = int(row['Door_num'] or 0)

        image_file = f"{brand.name}$${car_model.name}$${year}$${row['Color']}$${row['Adv_ID']}$$image_0.jpg"
        image_path = os.path.join(brand.name, str(year), image_file)
        if not os.path.exists(os.path.join(self.BASE_DIR, "car_images", image_path)):
            return None

        image_url = os.path.join(self.BASE_IMAGE_URL, image_path)

        return Car(
            car_model=car_model,
            price=price,
            engine_size=engine_size,
            image_url=image_url,
            gearbox=row['Gearbox'],
            fuel_type=row['Fuel_type'],
            color=row['Color'],
            year=year,
            mileage=mileage,
            seats=seats,
            doors=doors,
            body_type=row['Bodytype'],
        )

    def bulk_create_cars(self, cars_to_create):
        batch_size = 5000
        with transaction.atomic():
            for i in tqdm(range(0, len(cars_to_create), batch_size), desc="Creating cars"):
                Car.objects.bulk_create(cars_to_create[i:i + batch_size])

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(cars_to_create)} cars'))
        logger.info(f'Successfully loaded {len(cars_to_create)} cars')
