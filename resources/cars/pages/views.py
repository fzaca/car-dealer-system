from django.shortcuts import render
from django.core.paginator import Paginator

from resources.cars.models import Car, Brand, BodyType


def car_list_view(request):
    brand_filter = request.GET.get('brand', '')
    body_type_filter = request.GET.get('body_type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_year = request.GET.get('min_year', '')
    max_year = request.GET.get('max_year', '')

    cars = Car.objects.all()

    if brand_filter:
        cars = cars.filter(car_model__brand__name__icontains=brand_filter)

    if body_type_filter:
        cars = cars.filter(body_type__name__icontains=body_type_filter)

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)

    if min_year:
        cars = cars.filter(year__gte=min_year)

    if max_year:
        cars = cars.filter(year__lte=max_year)

    paginator = Paginator(cars, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    brands = Brand.objects.all()
    body_types = BodyType.objects.all()

    context = {
        'page_obj': page_obj,
        'brands': brands,
        'body_types': body_types,
        'brand_filter': brand_filter,
        'body_type_filter': body_type_filter,
        'min_price': min_price,
        'max_price': max_price,
        'min_year': min_year,
        'max_year': max_year,
    }

    return render(request, 'cars/car_list.html', context)
