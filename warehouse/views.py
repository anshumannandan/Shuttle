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
            bobj = Business.objects.get(name = self.request.GET.get('business'))
        except:
            raise CustomError("business doesn't exist")
        return bobj.warehouses.all()


class CountryListView(APIView):
    
    def get(self, request):
        return Response(get_country_list())


class warehouseRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.all()


class warehouseCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WarehouseSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class listCategoryView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class commodityRUDView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommoditySerializer

    def get_queryset(self):
        return Commodity.objects.filter(warehouse = self.request.GET.get('warehouse'))