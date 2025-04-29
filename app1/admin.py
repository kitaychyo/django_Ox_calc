from django.contrib import admin
from .models import SOx_save, NOx_save, NOx_fuel_save


@admin.register(SOx_save)
class SOx_saveAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'n1_SO2', 'n2_SO2', 'B', 'S_r', 'itog')

@admin.register(NOx_save)
class NOx_saveAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'Wr', 'Ar', 'Vr', 'Nd', 'specific_emissions')
    search_fields = ('name', 'burner_type', 'extra_fuel')
    list_filter = ('created_at', 'burner_type')

@admin.register(NOx_fuel_save)
class NOx_fuel_saveAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'T_ad', 'Bp', 'fuel_type', 'emission_power')
    search_fields = ('name', 'fuel_type')
    list_filter = ('created_at', 'fuel_type')