from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_index, name="user_index"),
    path('register', views.customer_registration, name="register"),
    path('choose_location', views.location_search, name="choose_location"),
    path('my/tickets', views.my_tickets, name="my_tickets"),
    path('register/account', views.register_owner_account, name="register_account"),
    path('login', views.login, name="login"),
    path('logout',views.logout_user, name="logout"),
    path('location/search',views.location_search, name="location_search"),
    path('confirm_ticket/<int:pk>',views.confirm_ticket, name="confirm_ticket"),
]