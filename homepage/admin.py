# Register your models here.
from django.contrib import admin
from .models import Subscriber, RecyclingHistory, AccountBalance, ContactSubmission
from .models import PickupRequest

# Register the models
admin.site.register(Subscriber)
admin.site.register(RecyclingHistory)
admin.site.register(AccountBalance)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'ready_for_pickup', 'status', 'created_at']
    list_filter = ['status']
    actions = ['mark_as_accepted', 'mark_as_completed']  

    def mark_as_accepted(self, request, queryset):
        queryset.update(status='Accepted')
    mark_as_accepted.short_description = "Mark selected requests as Accepted"

    def mark_as_completed(self, request, queryset):  
        queryset.update(status='Completed')
    mark_as_completed.short_description = "Mark selected requests as Completed"
