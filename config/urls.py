
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView

from core.views.avaliacao import avaliacao_ItemViewSet, avaliacao_UserViewSet
from core.views import ItemViewSet, CategoriaViewSet


router = DefaultRouter()
router.register(r"Avaliação Item", avaliacao_ItemViewSet)
router.register(r"Avaliação User", avaliacao_UserViewSet)
router.register(r"itens", ItemViewSet)
router.register(r"Categorias", CategoriaViewSet)

urlpatterns = [
    
    path("", RedirectView.as_view(url="admin/", permanent=False)),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
]
