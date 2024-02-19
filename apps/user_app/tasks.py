from celery import shared_task
from django.core.mail import send_mail
from .models import CustomUser
from utils.services.send_email import generate_code_for_send_mail


@shared_task
def user_created(user_id):
    user = CustomUser.objects.get(id=user_id)
    subject = "Mail confirmation {}".format(user_id)
    massage = "Dear {}\n\nyou have successfully registered, please confirm your e-mail. Enter the 4-digit code below {}".format(
        user.full_name, generate_code_for_send_mail()
    )
    mail_send = send_mail(subject, massage, "vanilla_sky@gmail.com", [user.email])
    return mail_send
