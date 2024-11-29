# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Subscriber
from django.core.exceptions import ValidationError

class SubscriberUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = Subscriber
        fields = ['fname', 'lname', 'email', 'phone', 'street_address', 'city', 'state', 'zip_code', 'payment_method']
        widgets = {
            'state': forms.Select(choices=[(state, state) for state in [
                'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
                'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
                'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
            ]]),
            'payment_method': forms.Select(choices=[
                ('paypal', 'PayPal'),
                ('venmo', 'Venmo'),
                ('check', 'Check'),
            ]),
        }

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not zip_code.isdigit() or len(zip_code) != 5:
            raise forms.ValidationError("Enter a valid 5-digit ZIP code.")
        return zip_code

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email).exclude(account_id=self.instance.account_id).exists():
            raise (forms.ValidationError
                   ("This email is already registered."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data


class UserRegistrationForm(UserCreationForm):
    fname = forms.CharField(max_length=100, label="First Name")
    lname = forms.CharField(max_length=100, label="Last Name")
    phone = forms.CharField(max_length=15, label="Phone Number")
    email = forms.EmailField(label="Email Address")
    street_address = forms.CharField(max_length=255, label="Street Address")
    city = forms.CharField(max_length=100, label="City")
    state = forms.ChoiceField(choices=[
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ], label="State")
    zip_code = forms.CharField(max_length=10, label="Zip Code")
    payment_method = forms.ChoiceField(choices=[
        ('paypal', 'PayPal'),
        ('venmo', 'Venmo'),
        ('check', 'Check')
    ], label="Payment Method")

    class Meta:
        model = User
        fields = ['username', 'fname', 'lname', 'email', 'phone', 'street_address', 'city', 'state', 'zip_code', 'payment_method', 'password1', 'password2']

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
                phone=self.cleaned_data['phone'],
                street_address=self.cleaned_data['street_address'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                zip_code=self.cleaned_data['zip_code'],
                payment_method=self.cleaned_data['payment_method']
            )
        return user


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}), required=True)