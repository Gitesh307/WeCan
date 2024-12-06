from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, SubscriberUpdateForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Subscriber
from .forms import ContactForm
from .models import ContactSubmission
from .models import PickupRequest
from .forms import PickupRequestForm

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
   if request.method == 'POST':
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(request, f'Your account has been created. You can log in now!')   
           return redirect('login')
   else:
       form = UserRegistrationForm()
   context = {'form': form}
   return render(request, 'register.html', context)

def login_view(request):
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

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

def settings(request):
    user = request.user

    # Fetch the subscriber for the logged-in user
    subscriber = Subscriber.objects.filter(account_id=request.user.id).first()
    if not subscriber:
        # Redirect to an error page if the subscriber profile is missing
        return render(request, "error.html", {"message": "No profile found!"})

    if request.method == 'POST':
        # Bind the submitted data to the form
        subscriber_form = SubscriberUpdateForm(request.POST, instance=subscriber)

        if subscriber_form.is_valid():
            # Save the subscriber updates
            updated_subscriber = subscriber_form.save(commit=False)

            # Update password if provided
            password = subscriber_form.cleaned_data.get('password')
            if password:
                updated_subscriber.password = make_password(password)

            # Save changes to the database
            updated_subscriber.save()

            messages.success(request, "Your changes have been saved successfully!")
            return redirect('settings')  # Redirect to the same page to prevent re-submission

        else:
            # Collect the first error and display it
            latest_error = None
            for field, errors in subscriber_form.errors.items():
                latest_error = f"{subscriber_form[field].label}: {errors[0]}"
                break
            messages.error(request, latest_error)

    else:
        # Pre-fill the form with the current subscriber data
        subscriber_form = SubscriberUpdateForm(instance=subscriber)

    context = {
        'subscriber_form': subscriber_form,
    }
    return render(request, 'settings.html', context)
