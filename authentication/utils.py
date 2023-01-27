import random, re
from . models import Email_OTP
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import APIException
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags


def validateOTP(user, otp, twofactoron=False, resetpass = False):
    if twofactoron:
        try:
            otpobject = user.twofactor.twofactorotp
            validity = 2
        except:
            return 'Please resend OTP'
    else:
        try:
            otpobject = user.emailotp
            validity = 5
        except:
            return 'Please resend Email OTP'
    if otpobject.created_time + timedelta(minutes=validity) < timezone.now():
        otpobject.delete()
        return 'OTP timed out'
    if otpobject.otp == int(otp):
        if twofactoron or resetpass:
            otpobject.delete()
        return 'OK'
    return 'OTP Invalid'


def send_email_otp(user):
    otp = random.randint(1000, 9999)
    mailaddress = user.email
    name = user.name
    html_content = render_to_string("sendotp.html", {"otp": otp,"name": name})
    send_email("Shuttle Password Reset", html_content, mailaddress)
    Email_OTP(
        user = user,
        otp = otp,
        created_time = timezone.now()
    ).save()


def resend_otp(user, twofactor = False):
    if twofactor:
        try:
            otpobject = user.twofactor.twofactorotp
        except:
            return True
    else:
        try:
            otpobject = user.emailotp
        except:
            return True
    if otpobject.created_time + timedelta(minutes=1) > timezone.now():
        return False
    otpobject.delete()
    return True


def validatePASS(password, email=None):
    if email is not None:
        user = authenticate(email=email, password=password)
        if user:
            return 'password same as previous one'
    reg = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!@#$]).{8,}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if not mat:
        return 'password conditions not fulfilled'
    return 'OK'


def normalize_email(email):  
        email = email or ''
        try:
            email_name, domain_part = email.lower().strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email


class CustomError(APIException):

    def __init__(self, error, code = status.HTTP_400_BAD_REQUEST):
        self.status_code = code
        self.detail = {'message' : [error]}


def send_email(subject, html_content, recepient):
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST,
            [recepient]
            )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return subject + ' EMAIL SENT'