from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import PickupRequest

@receiver(post_save, sender=PickupRequest)
def send_status_change_email(sender, instance, created, **kwargs):
    if created:
        subject = "Your Pickup Request Has Been Submitted!"
        message = (
            f"Hello {instance.user.first_name},\n\n"
            f"Your pickup request has been submitted successfully! "
            f"Our team will review it and notify you when it is accepted or completed. "
            f"Thank you for choosing WeCan for your recycling needs.\n\n"
            f"Best Regards,\nThe WeCan Team"
        )
        recipient_list = [instance.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

    elif instance.status == "Accepted":
        subject = "Your Pickup Request has been Accepted!"
        message = (
            f"Hello {instance.user.first_name},\n\n"
            f"Your pickup request has been accepted! "
            f"Thank you for recycling with WeCan.\n\n"
            f"Best Regards,\nThe WeCan Team"
        )
        recipient_list = [instance.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

    elif instance.status == "Picked Up":  
        subject = "Your Pickup Request has been Picked Up!"
        message = (
            f"Hello {instance.user.first_name},\n\n"
            f"Our team has successfully picked up your recyclables! "
            f"Thank you for your continued effort to make a positive environmental impact. "
            f"We appreciate your trust in WeCan.\n\n"
            f"Best Regards,\nThe WeCan Team"
        )
        recipient_list = [instance.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

    elif instance.status == "Completed":
        subject = "Your Pickup Request has been Completed!"
        message = (
            f"Hello {instance.user.first_name},\n\n"
            f"Your pickup request has been completed successfully! "
            f"We appreciate your contribution to recycling with WeCan.\n\n"
            f"Best Regards,\nThe WeCan Team"
        )
        recipient_list = [instance.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
