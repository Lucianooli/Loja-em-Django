from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.contrib import admin
from sistema_principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sistema_principal.urls')),
] 

