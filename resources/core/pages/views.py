from django.shortcuts import render

from resources.cars.models import Car
from resources.sales.models import Sale


def home_view(request):
    return render(request, 'home.html')


def dashboard_callback(request, context):
    cars_count = Car.objects.count()
    sales_count = Sale.objects.count()

    available_cars = Car.objects.filter(is_available=True)[:10]

    context.update({
        "cards": [
            {"title": "Total Cars", "metric": cars_count},
            {"title": "Total Sales", "metric": sales_count},
        ],
        "table_data": {
            "headers": ["Car Model", "Price", "Availability"],
            "rows": [
                [car.car_model.name, car.price, "Available" if car.is_available else "Sold"]
                for car in available_cars
            ]
        }
    })

    return context
