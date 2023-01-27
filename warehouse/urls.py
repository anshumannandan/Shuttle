from django.urls import path
from .views import *


urlpatterns = [
    path('list_business/', listBUSINESSView.as_view()),
    path('list_warehouses/', listWAREHOUSEView.as_view()),
    path('distance/', DistanceView.as_view()),
    path('countrylist/', CountryListView.as_view()),
]