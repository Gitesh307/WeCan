# models.py
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


class Role(models.TextChoices):
    SUBSCRIBER = 'Subscriber', 'Subscriber'
    DRIVER = 'Driver', 'Driver'
    REDEMPTION_WORKER = 'RedemptionCenterWorker', 'Redemption Center Worker'

class Subscriber(models.Model):
    linked_account = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='subscriber_profile', null = True)
    account_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255, default="")  
    city = models.CharField(max_length=100, default="")  
    state = models.CharField(max_length=2, default="NA")  
    zip_code = models.CharField(max_length=10, default="00000")  
    payment_method = models.CharField(max_length=10, default="paypal")  
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.fname
    
class QRCode(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='qr_codes')
    qr_image = models.ImageField(upload_to='qr_codes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.qr_image:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f'{self.subscriber.email}-{self.pk}')  
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            self.qr_image.save(f'{self.subscriber.fname}_qr_{self.pk}.png', ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)

class Driver(models.Model):
    linked_account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default='xyz@gmail.com')
    phone = models.CharField(max_length=15, default='111-000-000')

    def __str__(self):
        return self.name

class RedemptionWorker(models.Model):
    linked_account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default='abc@gmail.com')
    phone = models.CharField(max_length=15, default='000-000-000')

    def __str__(self):
        return self.name



class RecyclingHistory(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='recycling_history')
    date = models.DateTimeField(auto_now_add=True)
    items_recycled = models.IntegerField()  
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
    scanned_bag_count = models.PositiveIntegerField(default=0)  
    num_bags = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):

        super(PickupRequest, self).save(*args, **kwargs)

   

    def __str__(self):
        return f"Pickup Request by {self.user.username} - {self.status}"

    def calculate_points(self, num_items):
        """
        Calculate the points for the given number of items in a bag.
        Each item is worth 3.22 cents.
        """
        return round(num_items * 0.0322, 2)  
