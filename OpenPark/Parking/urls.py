from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.my_bookings, name="bookings"),
    path('dashboard', views.owner_dashboard, name="owner_dashboard"),
    path('bookings/car', views.my_car_bookings, name="my_car_bookings"),
    path('bookings/bike', views.my_bike_bookings, name="my_bike_bookings"),
    path('bookings/active', views.my_active_bookings, name="my_active_bookings"),
]
