from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('NOx/', views.NOx, name='NOx'),
    path('SOx/', views.SOx, name='SOx'),
    path('NOxFuel/', views.NOx_fuel, name='NOx_fuel'),
]
