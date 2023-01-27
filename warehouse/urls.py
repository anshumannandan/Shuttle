from django.urls import path
from .views import *


urlpatterns = [
    path('manage/', ManageWarehouseView.as_view()),
]