from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.my_bookings, name="bookings"),
    path('dashboard', views.owner_dashboard, name="owner_dashboard"),
]
