from django.db import models
from authentication.models import Business


class Warehouse(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='warehouses')
    location = models.CharField(max_length=255)
    volume = models.FloatField()


class Category(models.Model):
    name = models.CharField(max_length=255)


class Commodity(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name = 'commodities')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'category_commodities')
    name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField()
    volume = models.FloatField()
