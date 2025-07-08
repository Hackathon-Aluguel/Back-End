
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView



router = DefaultRouter()

urlpatterns = [
    
    path("", RedirectView.as_view(url="admin/", permanent=False)),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
]
