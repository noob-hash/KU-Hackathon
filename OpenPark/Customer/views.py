from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout, login as auth_login 
from Parking.models import Parking, KYC
from django.contrib import messages
import uuid
from Customer.models import Ticket
from django.contrib.auth.models import User

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
                return redirect('customer_dashboard')

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
            return redirect('choose_location')  # Replace 'home' with your desired URL name

    else:
        error_message = ""

    return render(request, 'Customer_registration.html', {'error_message': error_message})



def choose_location(request):
    return render(request, 'Customer/choose_location.html')

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
            owner = request.user 
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
            owner=request.user).values_list('code', flat=True)
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
            return redirect('owner_dashboard')  # Redirect to owner dashboard
        
    else:
        error_message = ""

    return render(request, 'Owner_registration.html', {'error_message': error_message})

