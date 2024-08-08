from resources.cars.models import BodyType, Brand


def body_types_processor(request):
    body_types = BodyType.objects.all()
    return {
        'body_types': body_types
    }


def brands_processor(request):
    brands = Brand.get_all_cached()
    return {
        'brands': brands
    }
