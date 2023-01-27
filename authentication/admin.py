from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import ModelAdmin


class BusinessAdmin(BaseUserAdmin):
    ordering = ['id', 'name']
    list_display = ['id', 'name', 'email']
    list_filter = ('is_superuser',)
    filter_horizontal = ()
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff',)}),
    )
    add_fieldsets = (
        ('User Credentials', {'fields': ('email', 'password1', 'password2')}),
        ('Personal Info', {'fields': ( 'name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff',)}),
    )

class EOAdmin(ModelAdmin):
    list_display = ['user', 'otp', 'created_time']


admin.site.register(Business, BusinessAdmin)
admin.site.register(Email_OTP, EOAdmin)