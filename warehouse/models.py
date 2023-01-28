from django.db import models
from authentication.models import Business
import datetime


class Warehouse(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='warehouses')
    location = models.CharField(max_length=255)
    volume = models.FloatField()
    occupied = models.FloatField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=255)


class Commodity(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name = 'commodities')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'category_commodities')
    name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField()
    volume = models.FloatField()


class Shipment(models.Model):
    sender = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name = 'senders')
    reciever = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name = 'recievers',null=True,blank=True)
    customer = models.CharField(max_length=255,null=True,blank=True)
    predicted_price = models.FloatField(blank=True,null=True)
    actual_price = models.FloatField(blank=True,null=True)
    proposal_date = models.DateTimeField(default=datetime.datetime(1000, 1, 1, 0, 0, 0))
    decision_date = models.DateTimeField(default=datetime.datetime(1000, 1, 1, 0, 0, 0))
    status = models.CharField(max_length=255,default='Pending',blank=True)