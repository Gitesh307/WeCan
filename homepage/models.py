# models.py

from django.db import models

class Subscriber(models.Model):
    account_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
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

