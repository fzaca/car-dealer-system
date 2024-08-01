from django.shortcuts import render

from resources.cars.models import Car, FeaturedCar
from resources.sales.models import Sale


def home_view(request):
    return render(request, 'home.html')


def dashboard_callback(request, context):
    cars_count = Car.objects.count()
    sales_count = Sale.objects.count()

    featured_cars = FeaturedCar.objects.select_related('car').all()[:10]

    recent_sales = Sale.objects.order_by('-date')[:10]

    context.update({
        "cards": [
            {"title": "Total Cars", "metric": cars_count},
            {"title": "Total Sales", "metric": sales_count},
        ],
        "cars_table_data": {
            "headers": ["Car Model", "Price", "Availability"],
            "rows": [
                [car.car.car_model.name, car.car.price, "Featured"]
                for car in featured_cars
            ]
        },
        "sales_table_data": {
            "headers": ["Sale ID", "Car Model", "Customer", "Date"],
            "rows": [
                [sale.hash, sale.car.car_model.name, sale.customer.user.username, sale.date.strftime("%Y-%m-%d %H:%M")]
                for sale in recent_sales
            ]
        }
    })

    return context
