# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
#
# class UserRegistrationForm(UserCreationForm):
#    first_name = forms.CharField(max_length=101)
#    last_name = forms.CharField(max_length=101)
#    email = forms.EmailField()
#    class Meta:
#        model = User
#        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Subscriber

class UserRegistrationForm(UserCreationForm):
    fname = forms.CharField(max_length=100, label="First Name")
    lname = forms.CharField(max_length=100, label="Last Name")
    phone = forms.CharField(max_length=15, label="Phone Number")
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'fname', 'lname', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['fname']
        user.last_name = self.cleaned_data['lname']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Create Subscriber instance
            Subscriber.objects.create(
                account_id=user.id,
                fname=self.cleaned_data['fname'],
                lname=self.cleaned_data['lname'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone']
            )
        return user
