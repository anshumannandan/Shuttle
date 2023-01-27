from rest_framework.generics import UpdateAPIView
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response({ **{'message' : ['Login Successful']}, **serializer.data}, status=status.HTTP_200_OK)


class SendOTPEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SendOTPEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message' : ['OTP sent on email']}, status=status.HTTP_200_OK)


class VerifyOTPEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message' : ['OTP Verified']}, status=status.HTTP_200_OK)


class ResetPasswordView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer
    
    def get_object(self):
        return Business.objects.filter(email = normalize_email(self.request.data.get('email')))

    def patch(self, request, *args, **kwargs):
        self.update(request,*args, **kwargs)
        return Response({'messsage':['Password changed successfully']}, status=status.HTTP_200_OK)