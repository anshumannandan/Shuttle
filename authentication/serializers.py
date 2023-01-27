from rest_framework.serializers import Serializer, EmailField, CharField, IntegerField
from django.contrib.auth import authenticate
from .models import Business
from .utils import *
from django.contrib.auth.hashers import make_password


class LoginSerializer(Serializer):
    email = EmailField(write_only = True)
    password = CharField(write_only = True)
    refresh = CharField(read_only = True)
    access = CharField(read_only = True)

    def validate(self,data):
        inemail = normalize_email(data['email'])
        if not Business.objects.filter(email = inemail).exists():
            raise CustomError('User not registered')
        user = authenticate(email=inemail, password=data['password'])
        if not user:
            raise CustomError('Invalid Credentials')
        data['refresh'] = user.refresh
        data['access'] = user.access
        return data


class SendOTPEmailSerializer(Serializer):
    email = EmailField()

    def validate(self, data):
        user = Business.objects.filter(email = normalize_email(data['email']))
        if not user.exists():
            raise CustomError('User not registered')
        user = user[0]
        if resend_otp(user):
            send_email_otp(user)
        return data


class VerifyOTPEmailSerializer(Serializer):
    email = EmailField()
    otp = IntegerField()

    def validate(self, data):
        user = Business.objects.filter(email = normalize_email(data['email']))
        if not user.exists():
            raise CustomError('User not registered')
        user = user[0]
        response = validateOTP(user, data['otp'])
        if response == 'OK':
            return data
        raise CustomError(response)


class ResetPasswordSerializer(Serializer):
    email = EmailField(write_only = True)
    otp = IntegerField(write_only = True)
    password = CharField()

    def validate(self, data):
        if not self.instance.exists():
            raise CustomError('User not registered')
        self.instance = self.instance[0]
        otpresponse = validateOTP(self.instance, data['otp'])
        if not otpresponse == 'OK' :
            raise CustomError('unauthorised access')
        passresponse = validatePASS(data['password'], self.instance.email)
        if not passresponse == 'OK':
            raise CustomError(passresponse)
        validateOTP(self.instance, data['otp'], resetpass = True)
        return data

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance
