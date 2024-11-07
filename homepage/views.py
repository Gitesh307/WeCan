from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Subscriber
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, "home.html", {})

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
def profile_view(request):
    try:
        # Attempt to fetch the subscriber using the user's email
        subscriber = Subscriber.objects.get(email=request.user.email)
        return render(request, 'profile.html', {'subscriber': subscriber})
    except Subscriber.DoesNotExist:
        # If no matching subscriber is found, show a user-friendly error message
        return HttpResponse("No subscriber profile found for this account. Please contact support.")
