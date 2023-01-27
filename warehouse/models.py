from django.db import models
from authentication.models import Business


class Warehouse(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='warehouses')
    location = models.CharField(max_length=255)
    size = models.FloatField()
    max_quantity = models.IntegerField()


class Category(models.Model):
    name = models.CharField(max_length=255)


class Commodity(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name = 'commodities')
    category = models.CharField(max_length=255)
    quantity = models.IntegerField()


class Shipment(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, related_name = 'shipments')
    reciever = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name = 'recievers')