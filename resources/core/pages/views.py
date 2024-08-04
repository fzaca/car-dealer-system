import json
import random
from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render
from django.db.models import Count
from django.utils.safestring import mark_safe

from resources.cars.models import Car, FeaturedCar, BodyType
from resources.sales.models import Sale


def home_view(request):
    body_types = BodyType.objects.all()

    featured_cars = list(FeaturedCar.objects.select_related('car').all())
    random_featured_cars = random.sample(featured_cars, min(len(featured_cars), 10))

    context = {
        'body_types': body_types,
        'featured_cars': random_featured_cars
    }

    return render(request, 'home.html', context)


def dashboard_callback(request, context):
    # Calcular fechas para la última semana
    today = timezone.now().date()
    one_week_ago = today - timedelta(days=6)  # Incluir hoy más 6 días hacia atrás

    # Contar ventas por día en la última semana
    sales_last_week = (
        Sale.objects
        .filter(created_at__date__range=[one_week_ago, today])
        .values('created_at__date')
        .annotate(sales_count=Count('id'))
        .order_by('created_at__date')
    )

    # Crear listas para las fechas y los conteos de ventas
    sales_dates = []
    sales_counts = []

    # Construir las listas de fechas y conteos
    for entry in sales_last_week:
        day = entry['created_at__date']
        sales_dates.append(day.strftime("%a"))  # Formatear a abreviatura del día
        sales_counts.append(entry['sales_count'])

    # Crear el diccionario de datos para el gráfico
    chart_data = {
        "labels": sales_dates,
        "datasets": [{
            "label": "Sales Count",
            "data": sales_counts,
            "borderColor": "#9333ea",
            "backgroundColor": "rgba(147, 51, 234, 0.2)",
            "fill": True,
            "tension": 0.1
        }]
    }

    # Serializar los datos del gráfico a JSON y marcarlos como seguros
    chart_data_json = mark_safe(json.dumps(chart_data))

    # Obtener conteos de autos y ventas
    cars_count = Car.objects.count()
    sales_count = Sale.objects.count()

    # Obtener autos destacados
    featured_cars = FeaturedCar.objects.select_related('car').all()[:10]

    # Obtener ventas recientes
    recent_sales = Sale.objects.order_by('-created_at')[:10]

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
                [sale.hash, sale.car.car_model.name, sale.customer.user.username, sale.created_at.strftime("%Y-%m-%d %H:%M")]
                for sale in recent_sales
            ]
        },
        "chart_data": chart_data_json  # Pasar datos serializados al contexto
    })

    return context
