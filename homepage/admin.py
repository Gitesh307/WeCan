# Register your models here.
from django.contrib import admin
from .models import Subscriber, RecyclingHistory, AccountBalance, ContactSubmission
from .models import PickupRequest, Driver, RedemptionWorker
from .models import Subscriber, QRCode

admin.site.register(Driver)
admin.site.register(RedemptionWorker)
admin.site.register(RecyclingHistory)
admin.site.register(AccountBalance)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'ready_for_pickup', 'num_bags', 'scanned_bag_count', 'status', 'created_at']
    list_filter = ['status']
    actions = ['mark_as_accepted', 'mark_as_picked_up', 'mark_as_completed']

    def mark_as_accepted(self, request, queryset):
        queryset.update(status='Accepted')
    mark_as_accepted.short_description = "Mark selected requests as Accepted"

    def mark_as_picked_up(self, request, queryset):
        queryset.update(status='Picked Up')  
    mark_as_picked_up.short_description = "Mark selected requests as Picked Up"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='Completed')
    mark_as_completed.short_description = "Mark selected requests as Completed"


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'phone', 'created_at')
    search_fields = ('fname', 'lname', 'email')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('qr_codes')

    def view_qr_codes(self, obj):
        return ", ".join([f'<img src="{qr.qr_image.url}" style="height: 100px;"/>' for qr in obj.qr_codes.all()])
    view_qr_codes.allow_tags = True
    view_qr_codes.short_description = 'QR Codes'

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'qr_image', 'created_at')