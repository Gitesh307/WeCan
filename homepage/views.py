from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SubscriberUpdateForm
from .forms import UserRegistrationForm, DriverRegistrationForm, RedemptionWorkerRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Subscriber, RecyclingHistory
from .forms import ContactForm
from .models import ContactSubmission,Subscriber, PickupRequest
from .forms import PickupRequestForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.

def home(request):
    return render(request, "home.html", {})

@login_required
def schedule(request):
    return render(request, 'schedule.html')

def services(request):
    return render(request, 'services.html') 

def contact(request):
    return render(request, 'contact.html') 

def resources(request):
    return render(request, 'resources.html') 

def works(request):
    return render(request, 'works.html') 

def who(request):
    return render(request, 'who.html') 

def policy(request):
    return render(request, 'policy.html') 

def terms(request):
    return render(request, 'terms.html') 

def blog(request):
    return render(request, 'blog.html') 

def faq(request):
    return render(request, 'faq.html') 

def gallery(request):
    return render(request, 'gallery.html') 

def volunteers(request):
    return render(request, 'volunteers.html')

def register(request):
    role = request.POST.get('role', None)
    subscriber_form = UserRegistrationForm(request.POST or None, request.FILES or None)
    driver_form = DriverRegistrationForm(request.POST or None)
    worker_form = RedemptionWorkerRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if role == 'Subscriber' and subscriber_form.is_valid():
            subscriber_form.save()
            messages.success(request, "Subscriber account created successfully!")
            return redirect('login')

        elif role == 'Driver' and driver_form.is_valid():
            driver_form.save()
            messages.success(request, "Driver account created successfully!")
            return redirect('login')

        elif role == 'RedemptionCenterWorker' and worker_form.is_valid():
            worker_form.save()
            messages.success(request, "Redemption Center Worker account created successfully!")
            return redirect('login')

        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'register.html', {
        'subscriber_form': subscriber_form,
        'driver_form': driver_form,
        'worker_form': worker_form,
    })


def custom_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Check if the user is a Driver
            if hasattr(user, 'driver_profile'):
                login(request, user)
                driver = user.driver_profile
                return render(request, 'driver_dashboard.html', {'driver': driver})

            # Check if the user is a Redemption Worker
            elif hasattr(user, 'worker_profile'):
                login(request, user)
                return redirect('worker_dashboard')
            else:
                login(request, user)
                return redirect('profile')  # Replace with subscriber dashboard URL

        else:
            # Invalid credentials
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')

    return render(request, 'login.html', {'form': form})



def login_view(request):
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def worker_dashboard(request):
    if not hasattr(request.user, 'worker_profile'):
        messages.error(request, "Access denied.")
        return redirect('login')

    worker = request.user.worker_profile
    subscribers = Subscriber.objects.all()

    if request.method == "POST":
        print(f"POST data: {request.POST}")

        subscriber_id = request.POST.get('subscriber_id')
        items_recycled = request.POST.get('items_recycled')
        points_earned = request.POST.get('points_earned')

        # Validate inputs
        if not subscriber_id or not items_recycled or not points_earned:
            messages.error(request, "All fields are required.")
            return redirect('worker_dashboard')

        try:
            items_recycled = int(items_recycled)
            points_earned = float(points_earned)

            # Fetch the subscriber and create recycling history
            subscriber = get_object_or_404(Subscriber, account_id=subscriber_id)
            RecyclingHistory.objects.create(
                subscriber=subscriber,
                items_recycled=items_recycled,
                points_earned=points_earned,
            )
            messages.success(request, f"Updated recycling history for {subscriber.fname} {subscriber.lname}.")
        except ValueError:
            messages.error(request, "Invalid number format for items recycled or points earned.")
        except Subscriber.DoesNotExist:
            messages.error(request, "Subscriber not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'worker_dashboard.html', {'worker': worker, 'subscribers': subscribers})


@login_required
def profile(request):
    # Get the Subscriber instance related to the logged-in user
    subscriber = get_object_or_404(Subscriber, account_id=request.user.id)
    subscriber.refresh_from_db()  # Fetch the latest data from the database
    return render(request, 'profile.html', {'subscriber': subscriber}) 


def contact_view(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            ContactSubmission.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            return redirect('contact_success') 
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def contact_success_view(request):
    return render(request, 'contact_success.html')

@login_required
def request_pickup(request):
    user = request.user
    pickup_request = PickupRequest.objects.filter(user=user).last()

    if request.method == "POST":
        form = PickupRequestForm(request.POST)
        if form.is_valid():
            ready_for_pickup = form.cleaned_data['ready_for_pickup']
            pickup_request = PickupRequest.objects.create(
                user=user,
                ready_for_pickup=ready_for_pickup,
                status="Pending"
            )
            return redirect('request_pickup')

    return render(request, 'request.html', {
        'pickup_request': pickup_request
    })

def pickuphistory(request):
    return render(request, 'pickuphistory.html') 


@login_required
def settings(request):
    subscriber = Subscriber.objects.filter(account_id=request.user.id).first()
    if not subscriber:
        return render(request, "error.html", {"message": "No profile found!"})

    if request.method == 'POST':
        subscriber_form = SubscriberUpdateForm(request.POST, request.FILES, instance=subscriber)

        if subscriber_form.is_valid():
            updated_subscriber = subscriber_form.save(commit=False)

            password = subscriber_form.cleaned_data.get('password')
            confirm_password = subscriber_form.cleaned_data.get('confirm_password')

            if password:
                if password == confirm_password:
                    try:
                        validate_password(password, user=subscriber.linked_account)
                        subscriber.linked_account.set_password(password)
                        subscriber.linked_account.save()
                    except ValidationError as e:
                        messages.error(request, f"Password error: {e}")
                        return render(request, 'settings.html', {'subscriber_form': subscriber_form})
                else:
                    messages.error(request, "Passwords do not match.")
                    return render(request, 'settings.html', {'subscriber_form': subscriber_form})

            updated_subscriber.save()
            messages.success(request, "Your changes have been saved successfully!")
            return redirect('settings')

        else:
            for field, errors in subscriber_form.errors.items():
                messages.error(request, f"{field}: {errors[0]}")
                break

    else:
        subscriber_form = SubscriberUpdateForm(instance=subscriber)

    context = {
        'subscriber_form': subscriber_form,
    }
    return render(request, 'settings.html', context)
