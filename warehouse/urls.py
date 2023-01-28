from django.urls import path
from .views import *


urlpatterns = [
    path('list_business/', listBUSINESSView.as_view()),
    path('list_warehouses/', listWAREHOUSEView.as_view()),
    path('countrylist/', CountryListView.as_view()),
    path('warehouseRUD/<int:pk>/', warehouseRUDView.as_view()),
    path('warehouseCREATE/', warehouseCreateView.as_view()),
    path('category/', listCategoryView.as_view()),
    path('commodityRUD/<int:pk>/', commodityRUDView.as_view()),
]