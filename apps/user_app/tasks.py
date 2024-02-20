from celery import shared_task
from django.core.mail import send_mail
from .models import CustomUser
from utils.services.send_email import generate_code_for_send_mail
from config.settings import email


@shared_task
def user_created(user_id):
    user = CustomUser.objects.get(id=user_id)
    subject = "Mail confirmation {}".format(user_id)
    massage = "Dear {}\n\nyou have successfully registered, please confirm your e-mail. Enter the 4-digit code below {}".format(
        user.full_name, generate_code_for_send_mail()
    )
    to_email = user.email
    from_email = email.EMAIL_HOST_USER
    send_mail(subject, massage, [from_email], [to_email], fail_silently=False)
    return user
