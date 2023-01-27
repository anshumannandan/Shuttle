from django.contrib import admin
from . models import *


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['business', 'location', 'max_quantity']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class CommodityAdmin(admin.ModelAdmin):
    list_display = ['warehouse', 'category', 'quantity']


admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Commodity, CommodityAdmin)