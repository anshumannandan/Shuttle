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