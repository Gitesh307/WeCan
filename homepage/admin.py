# Register your models here.
from django.contrib import admin
from .models import Subscriber, RecyclingHistory, AccountBalance, ContactSubmission

# Register the models
admin.site.register(Subscriber)
admin.site.register(RecyclingHistory)
admin.site.register(AccountBalance)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email')