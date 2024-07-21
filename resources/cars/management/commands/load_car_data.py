import csv
import logging
import os

import requests
from django.core.management.base import BaseCommand
from tqdm import tqdm

from resources.cars.models import Brand, CarModel, Trim

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Download and load car data from Google Drive CSV files'

    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data')
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
        self.load_trims()
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
            with open(os.path.join(self.BASE_DIR, 'Basic_table.csv'), newline='', encoding='utf-8') as csvfile:
                reader = list(csv.DictReader(csvfile))
                for row in tqdm(reader, desc="Loading brands"):
                    Brand.objects.get_or_create(name=row['Automaker'])
            logger.info('Successfully loaded brands')
        except Exception as e:
            logger.error(f'An error occurred while loading brands: {e}')
            self.stdout.write(self.style.ERROR('An error occurred while loading brands'))

    def load_car_models(self):
        try:
            with open(os.path.join(self.BASE_DIR, 'Basic_table.csv'), newline='', encoding='utf-8') as csvfile:
                reader = list(csv.DictReader(csvfile))
                for row in tqdm(reader, desc="Loading car models"):
                    brand = Brand.objects.get(name=row['Automaker'])
                    CarModel.objects.get_or_create(name=row['Genmodel'], brand=brand)
            logger.info('Successfully loaded car models')
        except Exception as e:
            logger.error(f'An error occurred while loading car models: {e}')
            self.stdout.write(self.style.ERROR('An error occurred while loading car models'))

    def load_trims(self):
        try:
            brands = {brand.name.lower(): brand for brand in Brand.objects.all()}
            car_models = {(car_model.name.lower(), car_model.brand.name.lower()): car_model for car_model in CarModel.objects.all()}

            trims_to_create = []

            with open(os.path.join(self.BASE_DIR, 'Trim_table.csv'), newline='', encoding='utf-8') as csvfile:
                reader = list(csv.DictReader(csvfile))
                for row in tqdm(reader, desc="Loading trims"):
                    try:
                        brand = brands.get(row['Maker'].lower())
                        if not brand:
                            logger.error(f'Brand not found: {row["Maker"]}')
                            continue

                        car_model_key = (row['Genmodel'].lower(), row['Maker'].lower())
                        car_model = car_models.get(car_model_key)
                        if not car_model:
                            car_model = CarModel.objects.create(name=row['Genmodel'], brand=brand)
                            car_models[car_model_key] = car_model

                        engine_size = self.parse_engine_size(row['Engine_size'])

                        trims_to_create.append(
                            Trim(
                                car_model=car_model,
                                name=row['Trim'],
                                year=row['Year'],
                                potential_price=row['Price'],
                                fuel_type=row['Fuel_type'],
                                engine_size=engine_size
                            )
                        )
                    except KeyError as e:
                        logger.error(f'Missing column in Trim_table.csv: {e}')
                        self.stdout.write(self.style.ERROR(f'Missing column in Trim_table.csv: {e}'))
                    except Exception as e:
                        logger.error(f'An error occurred while loading trims: {e}')
                        self.stdout.write(self.style.ERROR('An error occurred while loading trims'))

            Trim.objects.bulk_create(trims_to_create, ignore_conflicts=True)
            logger.info('Successfully loaded trims')
        except Exception as e:
            logger.error(f'An error occurred while loading trims: {e}')
            self.stdout.write(self.style.ERROR('An error occurred while loading trims'))