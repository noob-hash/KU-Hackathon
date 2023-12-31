from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout, login as auth_login 
from Parking.models import Parking, KYC
from django.contrib import messages
import uuid
from Customer.models import Ticket
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from io import BytesIO
import qrcode, string, json,random
from django.http import HttpResponse
from django.utils import timezone
from django.core.files.base import ContentFile
from Parking.models import Parking
from .models import ParkingReview


def generate_random_code():
    characters = string.digits  # Use only digits (0-9)
    code_length = 6
    random_code = ''.join(random.choice(characters) for _ in range(code_length))
    return random_code

# Create your views here.
def user_index(request):
    return render(request, 'index.html')

def logout_user(request):
    logout(request)
    return render(request, 'index.html')

def login(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('dashboard_customer')

        else:
            # Return an error response or render the login page with an error message
            message = "Incorrect Username or Password"

    context = {
        'message': message
    }
    
    # Handle GET request (display the login form)
    return render(request, 'Login.html', context)

def customer_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            error_message = "Username already taken."
        else:
            # Create a new user
            user = User.objects.create_user(username=username,email=email, password=password)
            user.save()

            # Authenticate and log in the user
            user = authenticate(username=username, password=password)
            auth_login(request, user)

            # Redirect to a success page or home page
            return redirect('location_search')  # Replace 'home' with your desired URL name

    else:
        error_message = ""

    return render(request, 'Customer_registration.html', {'error_message': error_message})


def my_tickets(request):
    user = request.user.username
    tickets = None
    if user:
        if Ticket.objects.filter(username=user).exists():
            tickets = Ticket.objects.filter(username=user)
        return render(request, 'Customer/my_bookings.html', {'tickets': tickets})
    else:
        return redirect('login')
    
def register_owner_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # first_name = request.POST['first_name']
        is_staff = True

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            error_message = "Username already taken."
        else:
            # Create a new user
            user = User.objects.create_user(username=username,email=email, password=password)
            # user.first_name = first_name
            user.is_staff = is_staff
            user.save()

            # Authenticate and log in the user

            code = str(uuid.uuid4().hex[:8])  
            owner = user 
            car_slot = int(request.POST.get('car_slot', 10))
            bike_slot = int(request.POST.get('bike_slot', 10))
            car_charge = int(request.POST.get('car_charge', 100))
            bike_charge = int(request.POST.get('bike_charge', 25))
            opening_time = request.POST.get('opening_time')
            close_time = request.POST.get('close_time')
            full_time = bool(request.POST.get('full_time', False))
            parking_type = request.POST.get('parking_type')
            latitude = float(request.POST.get('latitude', 0))
            longitude = float(request.POST.get('longitude', 0))
            image = request.FILES.get('image1')
            status = bool(request.POST.get('status', False))

            # Create a new Parking object and save it
            parking = Parking(
                code=code,
                owner=owner,
                car_slot=car_slot,
                bike_slot=bike_slot,
                car_charge=car_charge,
                bike_charge=bike_charge,
                opening_time=opening_time,
                close_time=close_time,
                full_time=full_time,
                parking_type=parking_type,
                latitude=latitude,
                longitude=longitude,
                image=image,
                status=status
            )
            parking.save()

            parking_code = Parking.objects.filter(
            owner=user).values_list('code', flat=True)
            citizenship_id = request.POST.get('citizenship_id')
            name = request.user
            image = request.FILES.get('image')
            phone = request.POST.get('phone')
            document_type = request.POST.get('document_type')
            address = request.POST.get('address')
            profile = request.FILES.get('profile')

            # Create a KYC entry
            kyc = KYC(
                parking_code=parking_code,
                citizenship_id=citizenship_id,
                name=name,
                image=image,
                phone=phone,
                document_type = document_type,
                address = address,
                profile=profile
            )
            kyc.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            messages.success(request, 'Registration successfully.')
            return redirect('dashboard')  # Redirect to owner dashboard
        
    else:
        error_message = ""

    return render(request, 'Owner_registration.html', {'error_message': error_message})

def location_search(request,pk=None):
    if request.method == 'POST':
        location = request.POST['location']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        vehicle_type = request.POST['vehicle_type']
        geolocator = Nominatim(user_agent="http")
        location2 = geolocator.geocode(location, timeout=None)
        lat = location2.latitude
        log = location2.longitude
        if location2:
            user_latitude = location2.latitude
            user_longitude = location2.longitude
            search_radius_km = 5  # Adjust this as needed
            parkings_within_radius = []

            all_parkings = Parking.objects.all()

            for parking in all_parkings:
                parking_latitude = parking.latitude
                parking_longitude = parking.longitude
                distance_km = geodesic((user_latitude, user_longitude), (parking_latitude, parking_longitude)).kilometers
                print(parking.name,distance_km)
                if distance_km <= search_radius_km:
                    try:
                        kyc = KYC.objects.get(parking_code=parking.code)
                        parking.kyc_name = kyc.name
                        parking.kyc_address = kyc.address
                    except KYC.DoesNotExist:
                        parking.kyc_name = None
                        parking.kyc_address = None

                    parkings_within_radius.append(parking)
            info = {
                'start_time': start_time,
                'end_time': end_time,
                'vehicle_type': vehicle_type,
                'location':location,
            }
            print(len(parkings_within_radius))
            ticket = None
            if pk:
                ticket = Parking.objects.get(id=pk)
                return redirect('book_ticket')
            return render(request, 'Makebooking.html', {'parkings': parkings_within_radius, 'lat': lat, 'log': log,"info":info,"tickets":ticket})

    return render(request, 'Customer.html')
   
def book_ticket(request):
    if request.method == 'POST':
        try:
            # parking = Parking.objects.get(code=parking_code)
            vehicle_type = request.POST.get('vehicle_type') 
            parking_code = request.POST.get('parking_code')
            arrivalTime = request.POST.get('start_time')
            departureTime = request.POST.get('end_time')
            username = request.user.username
            if vehicle_type=="Car":
                amount = request.POST.get('car_charge')
            else:
                amount = request.POST.get('bike_charge')
            info = {
                'parking_code': parking_code,
                'arrivalTime': arrivalTime,
                'arrivalTime': departureTime,
                'username': username,
            }
            img = qrcode.make(info)

            # Convert the QR code image to a Django ImageField
            img_io = BytesIO()
            img.save(img_io, format='PNG')  # Save the QR code as PNG

            ticket = Ticket.objects.create(
                code=generate_random_code(),
                username=request.user.username,
                status='Reserved',  # Set the initial status to Reserved
                booked_date=timezone.now(),
                amount = amount,
                arrivalTime = arrivalTime,
                departureTime = departureTime,
                parking_code = parking_code,
                vehicle_type = vehicle_type,
                # Other ticket fields here
            )

            # Attach the QR code image to the ticket's qr_code field
            ticket.qr_code.save(f'{ticket.pk}_qrcode.png', ContentFile(img_io.getvalue()), save=False)
            ticket.save()
            request.session['ticket_id'] = ticket.id

            return redirect('qr_generator')
        except Exception as e:
            # Handle exceptions as needed
            print(e)
            return HttpResponse('Error occurred while booking the ticket')
    else:
        # go to booking page
        return redirect('my_active_bookings') 

def qr_generator(request):
    try:
        ticket_id = request.session.get('ticket_id')
        del request.session['ticket_id']
        my_ticket = Ticket.objects.get(id=ticket_id)
        return render(request, 'QR.html', {"ticket": my_ticket})
    except Exception as e:
        return redirect('my_tickets')
   
def single_ticket(request, pk):
    user = request.user.username
    tickets = None
    if user:
        tickets = Ticket.objects.get(id=pk)
        return render(request, 'view.html', {'ticket': tickets})
    else:
        return redirect('login')
    
# review
def review(request,pk):
    try:
        reviews = ParkingReview.objects.filter(parking_code = pk)
        return render(request, 'review.html', {"reviews": reviews})
    except:
        message = "No such parking space exist"
        return render(request, 'review.html', {"error": message})
    
def addReview(request,pk):
    if request.method == "POST":
        user = request.user.username
        parking_code = pk
        rating = request.POST.get('rating') 
        comment = request.POST.get('comment') 

        review = ParkingReview.objects.create(
            parking_code = parking_code,
            user_code = user,
            rating = rating,
            comment = comment
        )

        review.save()
        return redirect(request, 'review/{parking_code}')
    
def feed(request):
    return render(request, 'VideoFeed.html')