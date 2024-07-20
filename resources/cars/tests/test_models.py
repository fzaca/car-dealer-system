import pytest

from resources.cars.models import Brand, CarModel, Trim


@pytest.mark.django_db  # noqa: PT023
def test_brand_str():
    brand = Brand(name="BMW")
    assert str(brand) == "BMW"


@pytest.mark.django_db  # noqa: PT023
def test_car_model_str():
    brand = Brand.objects.create(name="BMW")
    car_model = CarModel(name="Serie 2 Coupe", brand=brand)
    assert str(car_model) == "Serie 2 Coupe"


@pytest.mark.django_db  # noqa: PT023
def test_trim_str():
    brand = Brand.objects.create(name="BMW")
    car_model = CarModel.objects.create(name="Serie 2 Coupe", brand=brand)
    trim = Trim(
        car_model=car_model,
        name="230i",
        year=2022,
        price=35000.00,
        fuel_type="Gasoline",
        engine_size=2.00
    )
    assert str(trim) == "230i (2022)"
