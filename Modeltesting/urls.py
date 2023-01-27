from django.urls import path
from . import views
from Modeltesting.views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('predict/', TestView.as_view()),
]