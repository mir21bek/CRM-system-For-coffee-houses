import random


def generate_code_for_send_mail(length=4):
    otp = "".join(random.choice("0123456789") for _ in range(length))
    print(otp)
