# models.py
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


class Subscriber(models.Model):
    linked_account = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='subscriber_profile', null = True)
    account_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255, default="")  # Default empty string
    city = models.CharField(max_length=100, default="")  # Default empty string
    state = models.CharField(max_length=2, default="NA")  # Default to "NA"
    zip_code = models.CharField(max_length=10, default="00000")  # Default value
    payment_method = models.CharField(max_length=10, default="paypal")  # Default to "paypal"
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.fname

class RecyclingHistory(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='recycling_history')
    date = models.DateTimeField(auto_now_add=True)
    items_recycled = models.IntegerField()  # e.g., number of cans/bottles recycled
    points_earned = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Recycling history for {self.subscriber.fname} on {self.date}"

class AccountBalance(models.Model):
    subscriber = models.OneToOneField(Subscriber, on_delete=models.CASCADE, related_name='account_balance')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.subscriber.fname}'s balance"
    
class ContactSubmission(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    

class PickupRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Picked Up', 'Picked Up'),  
        ('Completed', 'Completed'),  
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ready_for_pickup = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            original_status = PickupRequest.objects.get(pk=self.pk).status
            if original_status != self.status and self.status == "Completed":
                self.add_to_recycling_history()
        super(PickupRequest, self).save(*args, **kwargs)

    def add_to_recycling_history(self):
        try:
            subscriber = Subscriber.objects.get(email=self.user.email)
        except Subscriber.DoesNotExist:
            raise ValueError(f"No Subscriber found for user with email: {self.user.email}")
        items_recycled = 10  
        points_earned = items_recycled * 0.5  

        RecyclingHistory.objects.create(
            subscriber=subscriber,
            items_recycled=items_recycled,
            points_earned=points_earned
        )

    def __str__(self):
        return f"Pickup Request by {self.user.username} - {self.status}"
