from django.contrib import admin
from . models import *


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['business', 'location']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class CommodityAdmin(admin.ModelAdmin):
    list_display = ['warehouse', 'category', 'quantity']

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['sender', 'reciever', 'status']


admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Shipment, ShipmentAdmin)