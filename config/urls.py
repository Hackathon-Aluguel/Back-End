from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from core.views.current_user import current_user

from core.views.google_logout import google_logout

from core.views.avaliacao import avaliacao_ItemViewSet, avaliacao_UserViewSet
from core.views.item import ItemViewSet, CategoriaViewSet, CondicaoViewSet
from core.views.aluguel import AluguelViewSet, Item_aluguelViewSet
from core.views.midia import MidiaViewSet, MidiaItemViewSet
from core.views.user import UserViewSet, UserCreateView, UserDetailView
from core.views.google_login_success import google_login_success

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"avaliacao_item", avaliacao_ItemViewSet)
router.register(r"avaliacao_user", avaliacao_UserViewSet)
router.register(r"itens", ItemViewSet)
router.register(r"categorias", CategoriaViewSet)
router.register(r"condicoes", CondicaoViewSet)
router.register(r"aluguel", AluguelViewSet)
router.register(r"itens_aluguel", Item_aluguelViewSet)
router.register(r"midia", MidiaViewSet)
router.register(r"midia_itens", MidiaItemViewSet)
router.register(r'usuarios', UserViewSet, basename='usuarios')

urlpatterns = [
    # Redireciona a raiz para admin
    path("", RedirectView.as_view(url="admin/", permanent=False)),

    # Rotas da API
    path("api/", include(router.urls)),

    # Admin
    path("admin/", admin.site.urls),

    # Registro customizado
    path("register/", UserCreateView.as_view(), name="register"),

    # JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # allauth
    path("accounts/", include("allauth.urls")),
    path('api/user-publico/<int:id>/', UserDetailView.as_view(), name='user-publico'),


    # Página de sucesso após login Google
    path("auth/google/success/", google_login_success, name="google_login_success"),

    path('users/me/', current_user),

    #logout
    path('google-logout/', google_logout, name='google-logout'),

    # dj-rest-auth registro
    path("auth/registration/", include("dj_rest_auth.registration.urls")),

    # Login social (Google) via allauth
    path("auth/social/", include("allauth.socialaccount.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
