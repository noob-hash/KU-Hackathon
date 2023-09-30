from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.my_bookings, name="bookings"),
    path('dashboard', views.owner_dashboard, name="dashboard"),
    path('dashboard_customer', views.customer_dashboard, name="customer_dashboard"),
    path('bookings_car', views.my_car_bookings, name="my_car_bookings"),
    path('bookings_bike', views.my_bike_bookings, name="my_bike_bookings"),
    path('bookings_active', views.my_active_bookings, name="my_active_bookings"),
]
