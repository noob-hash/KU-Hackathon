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
    path('choose_location/<int:pk>',views.location_search, name="choose_location"),
    path('my/qr', views.qr_generator, name="qr_generator"),  
    path('book_ticket', views.book_ticket, name="book_ticket"),
    path('ticket/<int:pk>', views.single_ticket, name="view"),
    path('review/<str:pk>', views.review, name="review"),
    path('addreview/<str:pk>', views.addReview, name="addreview"),
    path('owner/feed', views.feed, name="feed"),
]