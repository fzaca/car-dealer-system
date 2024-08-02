import pytest

from resources.cars.models import Car, CarModel, BodyType, Brand
from resources.users.models import CustomUser, Customer
from resources.sales.models import Sale, PaymentMethod, Payment, Invoice


CAR_PRICE = 25000.00
ENGINE_SIZE = 2.0
CAR_COLOR = "Blue"
CAR_YEAR = 2014
CAR_MILEAGE = 75000
CAR_SEATS = 5
CAR_DOORS = 5
CUSTOMER_PHONE = "123456789"
CUSTOMER_ADDRESS = "123 Main St"
CUSTOMER_DNI = "12345678"
PAYMENT_AMOUNT = 45147.40
PDF_URL = "https://example.com/invoice.pdf"


@pytest.mark.django_db  # noqa: PT023
def test_payment_creation():
    brand = Brand.objects.create(name="Renault")
    car_model = CarModel.objects.create(name="Grand Scenic", brand=brand)
    body_type = BodyType.objects.create(name="SUV")
    car = Car.objects.create(
        car_model=car_model,
        body_type=body_type,
        price=CAR_PRICE,
        engine_size=ENGINE_SIZE,
        image_url="https://example.com/path/to/image.jpg",
        gearbox="Automatic",
        fuel_type="Diesel",
        color=CAR_COLOR,
        year=CAR_YEAR,
        mileage=CAR_MILEAGE,
        seats=CAR_SEATS,
        doors=CAR_DOORS
    )
    user = CustomUser.objects.create_user(username="customer1", password="password")
    customer = Customer.objects.create(user=user, phone=CUSTOMER_PHONE, address=CUSTOMER_ADDRESS, dni=CUSTOMER_DNI)
    sale = Sale.objects.create(car=car, customer=customer)
    payment_method = PaymentMethod.objects.create(name="Credit Card")
    payment = Payment.objects.create(sale=sale, method=payment_method, amount=PAYMENT_AMOUNT)

    assert payment.sale.car == car
    assert payment.method.name == "Credit Card"
    assert payment.amount == PAYMENT_AMOUNT


@pytest.mark.django_db  # noqa: PT023
def test_invoice_creation():
    brand = Brand.objects.create(name="Renault")
    car_model = CarModel.objects.create(name="Grand Scenic", brand=brand)
    body_type = BodyType.objects.create(name="SUV")
    car = Car.objects.create(
        car_model=car_model,
        body_type=body_type,
        price=CAR_PRICE,
        engine_size=ENGINE_SIZE,
        image_url="https://example.com/path/to/image.jpg",
        gearbox="Automatic",
        fuel_type="Diesel",
        color=CAR_COLOR,
        year=CAR_YEAR,
        mileage=CAR_MILEAGE,
        seats=CAR_SEATS,
        doors=CAR_DOORS
    )
    user = CustomUser.objects.create_user(username="customer1", password="password")
    customer = Customer.objects.create(user=user, phone=CUSTOMER_PHONE, address=CUSTOMER_ADDRESS, dni=CUSTOMER_DNI)
    sale = Sale.objects.create(car=car, customer=customer)
    invoice = Invoice.objects.create(sale=sale, pdf_url=PDF_URL)

    assert invoice.sale.car == car
    assert invoice.pdf_url == PDF_URL
