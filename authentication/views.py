# import email
from rest_framework import status
from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.password_validation import validate_password
# from django.utils import timezone
# from rest_framework import generics
# from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import *
from .mail import *
from .models import *
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password



# def getTokens(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }

class Login_user(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = Business.objects.filter(email = email)
        if not user.exists():
            context = {'msg':'user with this email does not exist'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if user is not None:
            token = getTokens(user)
            return Response({'id':user.id,'token': token,'msg':'Login Success'}, status=status.HTTP_200_OK)

        return Response({'msg':'Enter correct Password'}, status=status.HTTP_400_BAD_REQUEST)