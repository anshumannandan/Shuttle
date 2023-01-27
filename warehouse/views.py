from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class listWAREHOUSEView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = listWAREHOUSEViewSerializer

    def get_queryset(self):
        queryset = Warehouse.objects.all().exclude(business = self.request.user)
        return queryset


class WAREHOUSEView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def get_queryset(self):
        print(self.request)
        return {}