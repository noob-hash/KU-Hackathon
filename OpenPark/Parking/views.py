from django.shortcuts import render,redirect

# Create your views here.
# admin site
def my_bookings(request):
    # if request.user.is_authenticated and request.user.is_staff:
    #     # Get all parking codes owned by the logged-in staff member
    #     owner_parking_codes = Parking.objects.filter(
    #         owner=request.user).values_list('code', flat=True)

    #     # Find all tickets that match the parking_code in the owner's parking codes
    #     parking_tickets = Ticket.objects.filter(
    #         parking_code__in=owner_parking_codes)
    # else:
    #     return redirect('login')

    return render(request, 'open_park/Owner.html', {'parking_tickets': parking_tickets})
