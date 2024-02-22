from celery import shared_task
from django.core.mail import send_mail

from apps.user_app.models import CustomUser
from config.settings import email
from utils.services.send_email import generate_code_for_send_mail
from django.utils import timezone


@shared_task()
def send_otp_code(user_id):
    user = CustomUser.objects.get(id=user_id)
    subject = f"Mail confirmation {user_id}"
    otp = generate_code_for_send_mail()
    user.otp = otp
    user.otp_expiration = timezone.now()
    user.save()
    message = (
        f"Dear {user.full_name}\n\nyou have successfully registered,"
        f" please confirm your e-mail. Enter the 4-digit code below\n\n{otp}"
    )
    to_email = user.email
    from_email = email.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [to_email], fail_silently=False)
    return user
