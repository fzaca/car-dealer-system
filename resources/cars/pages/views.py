from django.db.models import Max, Min
from django.core.paginator import Paginator
from django.shortcuts import render

from resources.cars.models import Car, Brand, CarModel


def car_list_view(request):  # noqa: PLR0914
    # Get filter values from request
    brand_filter = request.GET.get('brand', '')
    car_model_filter = request.GET.get('car_model', '')
    body_type_filter = request.GET.get('body_type', '')
    min_price = ''
    max_price = request.GET.get('max_price', '')
    min_year = request.GET.get('min_year', '')
    max_year = request.GET.get('max_year', '')

    # Initial car queryset
    cars = Car.objects.all()

    # Apply filters to the car queryset
    if brand_filter:
        cars = cars.filter(car_model__brand__name__icontains=brand_filter)

    if body_type_filter:
        cars = cars.filter(body_type__name__icontains=body_type_filter)

    if car_model_filter:
        cars = cars.filter(car_model__name__icontains=car_model_filter)

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)

    if min_year:
        cars = cars.filter(year__gte=min_year)

    if max_year:
        cars = cars.filter(year__lte=max_year)

    # Get maximum price and year range for filtering UI
    max_car_price = cars.aggregate(Max('price'))['price__max'] or 0
    default_max_price = max_car_price / 2 if max_car_price > 0 else 0
    min_car_year = cars.aggregate(Min('year'))['year__min'] or 0
    max_car_year = cars.aggregate(Max('year'))['year__max'] or 0

    # Pagination
    paginator = Paginator(cars, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all brands for the brand filter dropdown
    brands = Brand.objects.all()

    # Filter car models based on selected brand
    if brand_filter:
        car_models = CarModel.objects.filter(brand__name__icontains=brand_filter)
    else:
        car_models = CarModel.objects.all()

    context = {
        'page_obj': page_obj,
        'brands': brands,
        'car_models': car_models,
        'brand_filter': brand_filter,
        'body_type_filter': body_type_filter,
        'car_model_filter': car_model_filter,
        'min_price': min_price,
        'max_price': max_price,
        'min_year': min_year,
        'max_year': max_year,
        'max_car_price': max_car_price,
        'default_max_price': default_max_price,
        'min_car_year': min_car_year,
        'max_car_year': max_car_year,
    }

    return render(request, 'cars/car_list.html', context)
