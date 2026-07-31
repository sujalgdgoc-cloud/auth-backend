from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken

def generate_password_reset_token(user):
    token = AccessToken()

    token["user_id"] = user.id
    token["type"] = "password-reset"

    token.set_exp(lifetime = timedelta(minutes=15))

    return str(token)

def send_reset_email(user, token):
    reset_link = f"https://localhost:3000/reset-password/{token}"

    subject = "Password reset request!!"
    message = f"""
        Hi {user.username},

        Click the link below to reset your password.

        {reset_link}

        This link will expire in 15 minutes.

        If you didn't request a password reset, you can safely ignore this email.
        """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )