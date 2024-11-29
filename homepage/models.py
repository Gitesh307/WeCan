# models.py

from django.db import models

class Subscriber(models.Model):
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

    def __str__(self):
        return self.fname

class RecyclingHistory(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='recycling_history')
    date = models.DateTimeField(auto_now_add=True)
    items_recycled = models.IntegerField()  # e.g., number of cans/bottles recycled
    points_earned = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Recycling history for {self.subscriber.name} on {self.date}"

class AccountBalance(models.Model):
    subscriber = models.OneToOneField(Subscriber, on_delete=models.CASCADE, related_name='account_balance')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.subscriber.name}'s balance"
    
class ContactSubmission(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

