from django.urls import path
from .views import *


urlpatterns = [
    path('list/', listWAREHOUSEView.as_view()),
    path('warehouses/', WAREHOUSEView.as_view()),
]