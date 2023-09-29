from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.my_bookings, name="bookings"),
]
