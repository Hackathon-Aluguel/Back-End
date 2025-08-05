
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView

from core.views.avaliacao import avaliacao_ItemViewSet, avaliacao_UserViewSet
from core.views.item import ItemViewSet, CategoriaViewSet
from core.views.aluguel import AluguelViewSet, Item_aluguelViewSet
from core.views.midia import MidiaViewSet, Midia_itemViewSet
from core.views.user import UserViewSet


router = DefaultRouter()
router.register(r"avaliacao_item", avaliacao_ItemViewSet)
router.register(r"avaliacao_user", avaliacao_UserViewSet)
router.register(r"itens", ItemViewSet)
router.register(r"categorias", CategoriaViewSet)
router.register(r"aluguel", AluguelViewSet)
router.register(r"itens_aluguel", Item_aluguelViewSet)
router.register(r"midia", MidiaViewSet)
router.register(r"midia_itens", Midia_itemViewSet)
router.register(r"usuarios", UserViewSet)

urlpatterns = [
    path("", RedirectView.as_view(url="admin/", permanent=False)),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
]
