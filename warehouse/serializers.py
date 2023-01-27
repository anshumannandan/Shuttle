from .models import *
from rest_framework import serializers
from .utils import *
from authentication.utils import CustomError
import pandas


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['name', 'email']


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class DistanceSerializer(serializers.Serializer):
    con1 = serializers.CharField(max_length = 20)
    con2 = serializers.CharField(max_length = 20)

    def validate(self, data):
        condata = get_country_list()
        f1 = f2 = None
        for i in range(len(condata)):
            if condata[i] == data['con1']:
                f1 = i+1
            if condata[i] == data['con2']:
                f2 = i+1
        if f1 is None or f2 is None:
            raise CustomError('either of the countries in invalid')
        file = pandas.read_csv('files/distances.csv')
        data = file.to_csv().strip()
        distance = data.split('\n')[f1].strip()[2:].split(',')[f2]
        return distance