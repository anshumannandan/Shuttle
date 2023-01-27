from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from authentication.utils import CustomError
from .utils import get_country_list


class listBUSINESSView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessSerializer

    def get_queryset(self):
        return Business.objects.all().exclude(id = self.request.user.id)


class listWAREHOUSEView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        try:
            bobj = Business.objects.get(name = self.request.data['business'])
        except:
            raise CustomError("business doesn't exist")
        return bobj.warehouses.all()

class DistanceView(APIView):
    
    def post(self, request):
        serializer = DistanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response([data])


class CountryListView(APIView):
    
    def get(self, request):
        return Response(get_country_list())