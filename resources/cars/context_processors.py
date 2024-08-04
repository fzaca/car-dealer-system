from resources.cars.models import BodyType


def body_types_processor(request):
    body_types = BodyType.objects.all()
    return {
        'body_types': body_types
    }
