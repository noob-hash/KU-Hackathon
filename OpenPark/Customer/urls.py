from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_index, name="user_index"),
    path('register/parking', views.register_owner_parking, name="register_parking"),
    path('register/kyc', views.register_owner_kyc, name="register_kyc"),
    path('location/choose', views.choose_location, name="choose_location"),
    path('my/tickets', views.my_tickets, name="my_tickets"),
    path('register/account', views.register_owner_account, name="register_account"),
    path('login', views.login, name="login"),
]