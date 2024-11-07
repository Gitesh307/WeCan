# Register your models here.
from django.contrib import admin
from .models import Subscriber, RecyclingHistory, AccountBalance

# Register the models
admin.site.register(Subscriber)
admin.site.register(RecyclingHistory)
admin.site.register(AccountBalance)