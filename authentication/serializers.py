from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from dataclasses import field
from pyexpat import model
from django.core.exceptions import ValidationError
from authentication.models import email_otp, Business

class Verify_OTP_serializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    otp=