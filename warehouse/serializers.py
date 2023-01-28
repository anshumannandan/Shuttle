from .models import *
from rest_framework import serializers
from .utils import *
from authentication.utils import CustomError


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['name', 'email']


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

    def create(self, validated_data):
        validated_data['business'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['business'] = self.context['request'].user
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        bus_obj = Business.objects.get(id = data['business'])
        data['business'] = bus_obj.name
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        Warehouse_obj = validated_data['warehouse']
        add_space = validated_data['quantity'] * validated_data['volume']
        if add_space + Warehouse_obj.occupied > Warehouse_obj.volume:
            raise CustomError('Warehouse space exceeded')
        Warehouse_obj.occupied += add_space
        Warehouse_obj.save()
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = Category.objects.get(id = data['category']).name
        return data


class DistanceWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['location', 'volume', 'occupied']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        con1 = str(self.context['request'].GET.get('loc'))
        con2 = str(data['location'])
        data['distance'] = get_distance(con1, con2)
        return data


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

    def create(self, validated_data):
        commo = Commodity.objects.get(name = validated_data['commodity'])
        obj = Shipment.objects.create(
            sender = validated_data['sender'],
            commodity = commo.name,
            quantity = validated_data['quantity'],
        )
        con1 = validated_data['sender'].location
        try:
            con2 = validated_data['receiver'].location
            obj.reciever = validated_data['receiver']
        except:
            con2 = validated_data['customer']
            obj.customer = con2
        distance = get_distance(con1, con2)
        obj.predicted_price = predicted_price(obj.quantity, commo.volume, float(distance))
        obj.save()
        return obj

class ShipmentPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['actual_price']