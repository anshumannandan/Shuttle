from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import EmailValidator,MinValueValidator
from django.conf import settings

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None,):
        """
        Creates and saves a superuser with the given email,name and password.
        """
        user = self.create_user(
            email = email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Business(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',
        max_length=255,
        unique=True,
        validators=[EmailValidator()])
    name = models.CharField(max_length=150, default=None)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin
    
class email_otp(models.Model):
     email = models.EmailField(verbose_name='email address',
        max_length=255,
        unique=True,
        validators=[EmailValidator()], null=True)
     otp = models.CharField(max_length=4, blank=True, null=True)
     is_verified = models.BooleanField(default=False)
     time_created = models.DateTimeField(default=timezone.now)
     
     def __str__(self):
         return self.email
     
 