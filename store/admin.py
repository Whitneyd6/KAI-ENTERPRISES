from django.contrib import admin
from .models import Department, Equipment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'price', 'quantity_in_stock')
    list_filter = ('department',)
    search_fields = ('name',)