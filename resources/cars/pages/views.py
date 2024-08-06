from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse

from resources.cars.utils import get_filters, paginate_cars
from resources.cars.models import Car, Brand, CarModel


def car_list_view(request: HttpRequest) -> HttpResponse:
    filters = get_filters(request)

    cars = Car.filter_cars(filters)
    page_obj = paginate_cars(cars, filters['items_per_page'], filters['page_number'])

    aggregates = Car.get_aggregates()
    max_car_price = aggregates['max_price'] or 0
    default_max_price = max_car_price / 2 if max_car_price > 0 else 0
    min_car_year = aggregates['min_year'] or 0
    max_car_year = aggregates['max_year'] or 0

    brands = Brand.get_all_cached()
    car_models = CarModel.get_by_brand_cached(filters['brand'])

    context = {
        'page_obj': page_obj,
        'brands': brands,
        'car_models': car_models,
        'brand_filter': filters['brand'],
        'body_type_filter': filters['body_type'],
        'car_model_filter': filters['car_model'],
        'min_price': filters['min_price'],
        'max_price': filters['max_price'],
        'min_year': filters['min_year'],
        'max_year': filters['max_year'],
        'max_car_price': max_car_price,
        'default_max_price': default_max_price,
        'min_car_year': min_car_year,
        'max_car_year': max_car_year,
        'items_per_page': filters['items_per_page'],
    }

    return render(request, 'cars/car_list.html', context)


def car_detail_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    similar_cars = car.get_similar_cars()

    context = {
        'car': car,
        'similar_cars': similar_cars,
    }

    return render(request, 'cars/car_detail.html', context)
