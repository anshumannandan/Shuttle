from rest_framework.serializers import Serializer, EmailField, CharField, IntegerField, ModelSerializer
from django.contrib.auth import authenticate
from .models import Business, Sign_up_user
from .utils import *
from django.contrib.auth.hashers import make_password


class LoginSerializer(Serializer):
    email = EmailField(write_only = True)
    password = CharField(write_only = True)
    refresh = CharField(read_only = True)
    access = CharField(read_only = True)
    name = CharField(read_only = True)

    def validate(self,data):
        inemail = normalize_email(data['email'])
        if not Business.objects.filter(email = inemail).exists():
            raise CustomError('User not registered')
        user = authenticate(email=inemail, password=data['password'])
        if not user:
            raise CustomError('Invalid Credentials')
        data['refresh'] = user.refresh
        data['access'] = user.access
        data['name'] = user.name
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


class SignUPSerializer(ModelSerializer):
    class Meta:
        model = Sign_up_user
        fields = '__all__'

    def validate(self, data):
        try:
            Business.objects.get(email = data['email'])
        except:
            return data
        raise CustomError('User with this account already exist')


    def to_representation(self, instance):
        send_signup_otp(instance)
        return {'message' : ['OTP sent on mail']}


class VerifySignUpSerializer(Serializer):
    email = EmailField()
    otp = IntegerField()
    name = CharField(max_length = 255)
    password = CharField(max_length = 255)

    def validate(self, data):
        try:
            suu = Sign_up_user.objects.get(email = data['email'])
        except:
            raise CustomError('raise an otp first, does not exist')
        if suu.otp != data['otp']:
            raise CustomError('invalid otp')
        passresponse = validatePASS(data['password'])
        if not passresponse == 'OK':
            raise CustomError(passresponse)
        data['instance'] = suu
        return data

    def create(self, validated_data):
        obj = Business.objects.create(
            email = validated_data['email'],
            password = make_password(validated_data['password']),
            name = validated_data['name']
        )
        validated_data['instance'].delete()
        return validated_data
