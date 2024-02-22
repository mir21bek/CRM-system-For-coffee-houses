from celery import shared_task
from django.core.mail import send_mail

from apps.user_app.models import CustomUser
from config.settings import email
from utils.services.send_email import generate_code_for_send_mail


@shared_task()
def send_otp_code(user_id):
    user = CustomUser.objects.get(id=user_id)
    print("Before sending email")
    subject = "Mail confirmation {}".format(user_id)
    code = generate_code_for_send_mail()
    message = (
        f"Dear {user.email}\n\nyou have successfully registered,"
        f" please confirm your e-mail. Enter the 4-digit code below {code}"
    )
    to_email = user.email
    from_email = email.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [to_email], fail_silently=False)
    print("After sending email")
    return user
