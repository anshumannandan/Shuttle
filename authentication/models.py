from django.db.models.base import Model
from django.db.models.fields import BooleanField, EmailField, CharField, IntegerField, DateTimeField
from django.db.models.fields.related import OneToOneField
from django.db.models import CASCADE
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
import datetime


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Business(AbstractBaseUser):
    email = EmailField(max_length=255, unique=True)
    name = CharField(max_length=255)

    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def refresh(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh)

    def access(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_superuser
    

class Email_OTP(Model):
    user = OneToOneField(Business, on_delete=CASCADE, related_name='emailotp')
    otp = IntegerField(blank=True, null=True)
    created_time = DateTimeField(default=datetime.datetime(1000, 1, 1, 0, 0, 0))