from django.urls import path
from resources.cars.pages import views


urlpatterns = [
    path("", views.car_list_view, name="car_list"),
    path('<int:car_id>/', views.car_detail_view, name='car_detail'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment')
]
