from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')


def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context
