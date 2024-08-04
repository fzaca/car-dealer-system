from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Max, Min, Q
from resources.cars.models import Car, Brand, CarModel


def get_filters(request):
    filters = {
        'brand': request.GET.get('brand', ''),
        'car_model': request.GET.get('car_model', ''),
        'body_type': request.GET.get('body_type', ''),
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
        'min_year': request.GET.get('min_year', ''),
        'max_year': request.GET.get('max_year', ''),
        'items_per_page': int(request.GET.get('items_per_page', 12)),
        'page_number': request.GET.get('page', 1)
    }

    try:
        filters['min_price'] = float(filters['min_price']) if filters['min_price'] else None
    except ValueError:
        filters['min_price'] = None

    try:
        filters['max_price'] = float(filters['max_price']) if filters['max_price'] else None
    except ValueError:
        filters['max_price'] = None

    try:
        filters['min_year'] = int(filters['min_year']) if filters['min_year'] else None
    except ValueError:
        filters['min_year'] = None

    try:
        filters['max_year'] = int(filters['max_year']) if filters['max_year'] else None
    except ValueError:
        filters['max_year'] = None

    return filters


def filter_cars(filters):
    cache_key = f"cars_{filters['brand']}_{filters['car_model']}_{filters['body_type']}_" \
                f"{filters['min_price']}_{filters['max_price']}_" \
                f"{filters['min_year']}_{filters['max_year']}_{filters['items_per_page']}_{filters['page_number']}"

    cars = cache.get(cache_key)
    if cars is None:
        cars = Car.objects.select_related('car_model', 'car_model__brand', 'body_type')

        q_filters = Q()
        if filters['brand']:
            q_filters &= Q(car_model__brand__name__icontains=filters['brand'])
        if filters['car_model']:
            q_filters &= Q(car_model__name__icontains=filters['car_model'])
        if filters['body_type']:
            q_filters &= Q(body_type__name__icontains=filters['body_type'])
        if filters['min_price'] is not None:
            q_filters &= Q(price__gte=filters['min_price'])
        if filters['max_price'] is not None:
            q_filters &= Q(price__lte=filters['max_price'])
        if filters['min_year'] is not None:
            q_filters &= Q(year__gte=filters['min_year'])
        if filters['max_year'] is not None:
            q_filters &= Q(year__lte=filters['max_year'])

        cars = cars.filter(q_filters)

        cache.set(cache_key, cars, timeout=300)
    return cars


def get_aggregates():
    cache_key = "cars_aggregates"
    aggregates = cache.get(cache_key)
    if not aggregates:
        aggregates = Car.objects.aggregate(
            max_price=Max('price'),
            min_year=Min('year'),
            max_year=Max('year')
        )
        cache.set(cache_key, aggregates, timeout=300)
    return aggregates


def get_brands():
    cache_key = "brands"
    brands = cache.get(cache_key)
    if brands is None:
        brands = Brand.objects.all()
        cache.set(cache_key, brands, timeout=300)
    return brands


def get_car_models(brand_filter):
    cache_key = f"car_models_{brand_filter}"
    car_models = cache.get(cache_key)
    if car_models is None:
        if brand_filter:
            car_models = CarModel.objects.filter(brand__name__icontains=brand_filter)
        else:
            car_models = CarModel.objects.all()
        cache.set(cache_key, car_models, timeout=300)
    return car_models


def paginate_cars(cars: list, items_per_page: int, page_number: int) -> Paginator:
    paginator = Paginator(cars, items_per_page)
    page_obj = paginator.get_page(page_number)
    return page_obj
