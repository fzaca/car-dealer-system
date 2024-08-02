import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from resources.cars.models import Car
from resources.users.models import Customer, CustomUser
from resources.sales.models import Sale, PaymentMethod, Payment, Invoice

fake = Faker()


class Command(BaseCommand):
    help = 'Load random data into Sale, PaymentMethod, Payment, and Invoice models'

    def handle(self, *args, **kwargs):
        self.clear_existing_data()
        self.load_customers()
        self.load_payment_methods()
        self.load_sales()

    def clear_existing_data(self):
        Sale.objects.all().delete()
        Payment.objects.all().delete()
        Invoice.objects.all().delete()
        PaymentMethod.objects.all().delete()
        Customer.objects.all().delete()
        CustomUser.objects.filter(is_customer=True).delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared existing data'))

    def load_customers(self):
        users = []
        customers = []

        for _ in range(50):
            user = CustomUser(
                username=fake.user_name(),
                email=fake.email(),
                is_customer=True
            )
            user.set_password('password')
            users.append(user)

        CustomUser.objects.bulk_create(users)

        for user in CustomUser.objects.filter(is_customer=True):
            customer = Customer(
                user=user,
                phone=fake.phone_number(),
                address=fake.address(),
                dni=fake.unique.random_number(digits=8)
            )
            customers.append(customer)

        Customer.objects.bulk_create(customers)
        self.stdout.write(self.style.SUCCESS('Successfully loaded customers'))

    def load_payment_methods(self):
        methods = ['Credit Card', 'Debit Card', 'Cash', 'Bank Transfer']
        payment_methods = [PaymentMethod(name=method) for method in methods]
        PaymentMethod.objects.bulk_create(payment_methods)
        self.stdout.write(self.style.SUCCESS('Successfully loaded payment methods'))

    def load_sales(self):  # noqa: PLR0914
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

        now = timezone.now()
        one_week_ago = now - timezone.timedelta(days=7)

        sales = []
        payments = []
        invoices = []

        for _ in range(50):
            car = random.choice(cars)
            customer = random.choice(customers)

            created_at = fake.date_time_between(start_date=one_week_ago, end_date=now, tzinfo=timezone.get_current_timezone())

            sale = Sale(car=car, customer=customer, created_at=created_at)
            sale.save()
            sales.append(sale)

            method = random.choice(payment_methods)
            amount = random.uniform(5000, 50000)
            payment = Payment(sale=sale, method=method, amount=amount, created_at=created_at)
            payment.save()
            payments.append(payment)

            pdf_url = fake.url()
            invoice = Invoice(sale=sale, pdf_url=pdf_url, created_at=created_at)
            invoice.save()
            invoices.append(invoice)

        self.stdout.write(self.style.SUCCESS('Successfully loaded random sales, payments, and invoices'))
