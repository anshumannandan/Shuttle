from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class ManageWarehouseView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ManageWarehouseSerializer
    queryset = Warehouse.objects.all()