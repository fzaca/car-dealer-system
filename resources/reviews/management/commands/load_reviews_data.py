import random

from django.core.management.base import BaseCommand
from faker import Faker

from resources.cars.models import Car
from resources.sales.models import Sale
from resources.users.models import Customer
from resources.reviews.models import Review, Comment

fake = Faker()


class Command(BaseCommand):
    help = 'Load random data into Review and Comment models'

    def handle(self, *args, **kwargs):
        self.clear_existing_data()
        self.load_reviews()
        self.load_comments()

    def clear_existing_data(self):
        Review.objects.all().delete()
        Comment.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared existing data'))

    def load_reviews(self):
        sales = list(Sale.objects.all())
        customers = list(Customer.objects.all())

        if not sales:
            self.stdout.write(self.style.ERROR('No sales found'))
            return
        if not customers:
            self.stdout.write(self.style.ERROR('No customers found'))
            return

        reviews = []

        existing_combinations = set()

        for _ in range(100):
            sale = random.choice(sales)
            customer = random.choice(customers)

            if (customer.id, sale.id) in existing_combinations:
                continue

            review = Review(
                customer=customer,
                sale=sale,
                rating=random.randint(1, 10),
                comment=fake.text(max_nb_chars=200),
            )
            reviews.append(review)

            # Añadir la combinación al set para evitar duplicados
            existing_combinations.add((customer.id, sale.id))

        Review.objects.bulk_create(reviews)
        self.stdout.write(self.style.SUCCESS('Successfully loaded reviews'))

    def load_comments(self):
        cars = list(Car.objects.all())
        customers = list(Customer.objects.all())

        if not cars:
            self.stdout.write(self.style.ERROR('No cars found'))
            return
        if not customers:
            self.stdout.write(self.style.ERROR('No customers found'))
            return

        comments = []

        for _ in range(100):
            car = random.choice(cars)
            customer = random.choice(customers)

            comment = Comment(
                customer=customer,
                car=car,
                content=fake.text(max_nb_chars=500),
            )
            comments.append(comment)

        Comment.objects.bulk_create(comments)
        self.stdout.write(self.style.SUCCESS('Successfully loaded comments'))
