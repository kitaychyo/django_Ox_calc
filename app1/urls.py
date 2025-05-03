from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('NOx/', views.NOx, name='NOx'),
    path('SOx/', views.SOx, name='SOx'),
    path('NOxFuel/', views.NOx_fuel, name='NOx_fuel'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
