
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView

from core.views import avaliacao_ItemViewSet, avaliacao_UserViewSet

router = DefaultRouter()
router.register(r"Avaliação Item", avaliacao_ItemViewSet)
router.register(r"Avaliação User", avaliacao_UserViewSet)

urlpatterns = [
    
    path("", RedirectView.as_view(url="admin/", permanent=False)),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
]
