import imp
from django.urls import path
from .models import Business
from . import views
from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', Login_user.as_view(), name='token_obtain_pair'),
]