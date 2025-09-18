from django.contrib import admin 
from django.urls import include, path 
from django.views.generic import RedirectView 
from django.conf import settings 
from django.conf.urls.static import static 

from rest_framework.routers import DefaultRouter 
from core.views.current_user import current_user 
from core.views.avaliacao import avaliacao_ItemViewSet, avaliacao_UserViewSet 
from core.views.item import ItemViewSet, CategoriaViewSet 
from core.views.aluguel import AluguelViewSet, Item_aluguelViewSet 
from core.views.midia import MidiaViewSet, Midia_itemViewSet 
from core.views.user import UserViewSet, UserCreateView 
from core.views.google_login_success import google_login_success 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from a_rtchat.views import get_or_create_chatroom, chat_view, chat_file_upload


from a_users.views import (
    profile_view,
    profile_edit_view,
    profile_settings_view,
    UserDetailView
)









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

urlpatterns = [ # Redireciona a raiz para admin 
               path("", RedirectView.as_view(url="admin/", permanent=False)), # Rotas da API 
               path("admin/", admin.site.urls), # Registro customizado 
               path("register/", UserCreateView.as_view(), name="register"), # JWT 
               path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
               path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # allauth 
               path("accounts/", include("allauth.urls")), # Página de sucesso após login Google 
               path("auth/google/success/", google_login_success, name="google_login_success"), 
               path('users/me/', current_user), # dj-rest-auth registro 
               path("auth/registration/", include("dj_rest_auth.registration.urls")), # Login social (Google) via allauth 
               path("auth/social/", include("allauth.socialaccount.urls")), #chat 
               path('chat/', include('a_rtchat.urls')), 
               path('profile/', include('a_users.urls')), 
               path('@<username>/', profile_view, name="profile"), 




    # Rotas da API
    path("api/", include(router.urls)),

    # Usuário logado
    path("api/users/me/", current_user, name="current-user"),

    # Registro customizado
    path("api/register/", UserCreateView.as_view(), name="register"),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Profile endpoints REST
    path("api/profile/<str:username>/", UserDetailView.as_view(), name="profile-detail"),
    path("api/profile/<str:username>/edit/", profile_edit_view, name="profile-edit"),
    path("api/profile/settings/", profile_settings_view, name="profile-settings"),

    # Chat endpoints REST
    path("api/chat/<str:username>/", get_or_create_chatroom, name="start-chat"),
    path("api/chat/room/<str:chatroom_name>/", chat_view, name="chatroom"),
    path("api/chat/fileupload/<str:chatroom_name>/", chat_file_upload, name="chat-file-upload"),
    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [ path("__reload__/", include("django_browser_reload.urls")), ]