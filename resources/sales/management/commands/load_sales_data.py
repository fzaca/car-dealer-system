import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from resources.cars.models import Car
from resources.users.models import Customer
from resources.sales.models import Sale, PaymentMethod, Payment, Invoice


fake = Faker()


class Command(BaseCommand):
    help = 'Load random data into Sale, PaymentMethod, Payment, and Invoice models'

    def handle(self, *args, **kwargs):
        self.load_payment_methods()
        self.load_sales()

    def load_payment_methods(self):
        methods = ['Credit Card', 'Debit Card', 'Cash', 'Bank Transfer']
        for method in methods:
            PaymentMethod.objects.get_or_create(name=method)
        self.stdout.write(self.style.SUCCESS('Successfully loaded payment methods'))

    def load_sales(self):
        cars = list(Car.objects.filter(is_available=True))
        customers = list(Customer.objects.all())
        payment_methods = list(PaymentMethod.objects.all())

        if not cars:
            self.stdout.write(self.style.ERROR('No available cars found'))
            return
        if not customers:
            self.stdout.write(self.style.ERROR('No customers found'))
            return
        if not payment_methods:
            self.stdout.write(self.style.ERROR('No payment methods found'))
            return

        for _ in range(50):
            car = random.choice(cars)
            customer = random.choice(customers)
            sale_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=timezone.get_current_timezone())

            sale = Sale.objects.create(car=car, customer=customer, date=sale_date)

            method = random.choice(payment_methods)
            amount = random.uniform(5000, 50000)
            payment_date = sale_date

            Payment.objects.create(sale=sale, method=method, amount=amount, date=payment_date)

            pdf_url = fake.url()
            Invoice.objects.create(sale=sale, pdf_url=pdf_url, date=sale_date)

            car.is_available = False
            car.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded random sales, payments, and invoices'))
