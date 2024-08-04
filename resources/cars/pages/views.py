from django.shortcuts import render


def car_list_view(request):
    return render(request, 'cars/car_list.html')
