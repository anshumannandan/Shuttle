from .models import *
from rest_framework import serializers


class listWAREHOUSEViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        business_obj = Business.objects.get(id = data['business'])
        data['business'] = business_obj.name
        return data