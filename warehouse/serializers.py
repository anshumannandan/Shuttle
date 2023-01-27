from .models import *
from rest_framework import serializers


class ManageWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'