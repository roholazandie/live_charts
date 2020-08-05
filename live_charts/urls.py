from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url

urlpatterns = [
    path('main/', include('linechart.urls')),
    path('random_generator/', include('linechart.urls')),
    path('admin/', admin.site.urls),
]
