from django.core.paginator import Paginator


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


def paginate_cars(cars: list, items_per_page: int, page_number: int) -> Paginator:
    paginator = Paginator(cars, items_per_page)
    page_obj = paginator.get_page(page_number)
    return page_obj
