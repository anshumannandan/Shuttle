from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
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
            return bobj.warehouses.all()
        except:
            return Warehouse.objects.all()


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


class commodityRUDView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommoditySerializer

    def get_queryset(self):
        return Commodity.objects.filter(warehouse = self.request.GET.get('warehouse'))


class ListDistanceView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DistanceWarehouseSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return Warehouse.objects.all().exclude(business = self.request.user)

class AdminView(APIView):
    def patch(self,request,pk):
        shipment = Shipment.objects.get(id=pk)
        ser = ShipmentPriceSerializer(data = request.data)
        ser.is_valid(raise_exception = True)
        shipment.actual_price = ser.data['actual_price']
        shipment.save()
        return Response(shipment.actual_price)

    def get(self,request,pk,st):
        shipment = Shipment.objects.filter(id=pk)
        if len(shipment)!=0:
            shipment = Shipment.objects.get(id=pk)
            if st == 0:
                shipment.status = 'Denied'
                shipment.save()
                return Response("shipment denied")
            shipment.status = 'Allowed'
            shipment.save()
            return Response("shipment approved")
        return Response("id not found")


class ShipmentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        return Shipment.objects.all()
