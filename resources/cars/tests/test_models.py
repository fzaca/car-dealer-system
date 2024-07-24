import pytest

from resources.cars.models import Brand, Car, CarModel


@pytest.mark.django_db  # noqa: PT023
def test_brand_str():
    brand = Brand(name="BMW")
    assert str(brand) == "BMW"


@pytest.mark.django_db  # noqa: PT023
def test_car_model_str():
    brand = Brand.objects.create(name="BMW")
    car_model = CarModel.objects.create(name="Serie 2 Coupe", brand=brand)
    assert str(car_model) == "Serie 2 Coupe"


@pytest.mark.django_db  # noqa: PT023
def test_car_str():
    brand = Brand.objects.create(name="BMW")
    car_model = CarModel.objects.create(name="Serie 2 Coupe", brand=brand)
    car = Car.objects.create(
        car_model=car_model,
        price=35000.00,
        engine_size=2.00,
        image_url="https://example.com/path/to/image.jpg",
        gearbox="Manual",
        fuel_type="Gasolina",
        color="Black",
        year=2022,
        mileage=0,
        seats=4,
        doors=2,
        body_type="Coupe"
    )
    assert str(car) == "Serie 2 Coupe (2022)"
