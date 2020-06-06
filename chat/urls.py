from django.urls import include, path
from django.contrib import admin
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apis_v1.urls')),
]
