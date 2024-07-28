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
        self.clear_existing_data()
        self.load_payment_methods()
        self.load_sales()

    def clear_existing_data(self):
        Sale.objects.all().delete()
        Payment.objects.all().delete()
        Invoice.objects.all().delete()
        PaymentMethod.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared existing data'))

    def load_payment_methods(self):
        methods = ['Credit Card', 'Debit Card', 'Cash', 'Bank Transfer']
        payment_methods = [PaymentMethod(name=method) for method in methods]
        PaymentMethod.objects.bulk_create(payment_methods)
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

        sales = []
        payments = []
        invoices = []

        for _ in range(50):
            car = random.choice(cars)
            customer = random.choice(customers)
            sale_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=timezone.get_current_timezone())

            sale = Sale(car=car, customer=customer, date=sale_date)
            sales.append(sale)

        Sale.objects.bulk_create(sales)

        for sale in sales:
            method = random.choice(payment_methods)
            amount = random.uniform(5000, 50000)
            payment_date = sale.date

            payment = Payment(sale=sale, method=method, amount=amount, date=payment_date)
            payments.append(payment)

            pdf_url = fake.url()
            invoice = Invoice(sale=sale, pdf_url=pdf_url, date=sale.date)
            invoices.append(invoice)

        Payment.objects.bulk_create(payments)
        Invoice.objects.bulk_create(invoices)

        self.stdout.write(self.style.SUCCESS('Successfully loaded random sales, payments, and invoices'))
