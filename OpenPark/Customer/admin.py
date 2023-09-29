from django.contrib import admin
from Parking.models import Parking,KYC
from .models import Ticket,ParkingReview

# Register your models here.

admin.site.register(Ticket)
admin.site.register(Parking)
admin.site.register(KYC)
admin.site.register(ParkingReview)