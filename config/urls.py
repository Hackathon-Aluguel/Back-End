
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
 
from core.views.user import UserViewSet, UserCreateView 
from core.views.google_login_success import google_login_success 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from a_users.views import (
    profile_view,
    profile_edit_view,
    profile_settings_view,
    UserDetailView
)


from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from core.views.google_logout import google_logout

from core.views.avaliacao import avaliacao_ItemViewSet, avaliacao_UserViewSet
from core.views.item import ItemViewSet, CategoriaViewSet, CondicaoViewSet
from core.views.aluguel import AluguelViewSet, Item_aluguelViewSet
from core.views.midia import MidiaViewSet, MidiaItemViewSet
from core.views.user import UserViewSet, UserCreateView, UserDetailView
from core.views.google_login_success import google_login_success

from a_users.views import UserViewSet

from a_rtchat import views



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
    path("", RedirectView.as_view(url="admin/", permanent=False)),
    path("auth/google/success/", google_login_success, name="google_login_success"), 
    path("admin/", admin.site.urls), # Registro customizado 
    path("register/", UserCreateView.as_view(), name="register"), 

    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("accounts/", include("allauth.urls")),  
    
    path('users/me/', current_user),  
    path("auth/registration/", include("dj_rest_auth.registration.urls")),  

    path("auth/social/", include("allauth.socialaccount.urls")), 
    path('profile/', include('a_users.urls')), 
    path('@<username>/', profile_view, name="profile"), 

   
    path("api/", include(router.urls)),

   
    path("api/users/me/", current_user, name="current-user"),

    
    path("api/register/", UserCreateView.as_view(), name="register"),

   
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

   
    path("api/profile/<str:username>/", UserDetailView.as_view(), name="profile-detail"),
    path("api/profile/<str:username>/edit/", profile_edit_view, name="profile-edit"),
    path("api/profile/settings/", profile_settings_view, name="profile-settings"),
   
    path("accounts/", include("allauth.urls")),
    path('api/user-publico/<int:id>/', UserDetailView.as_view(), name='user-publico'),
    
    



    
    path('google-logout/', google_logout, name='google-logout'),

   
    path("auth/registration/", include("dj_rest_auth.registration.urls")),


    
    path("auth/social/", include("allauth.socialaccount.urls")),
    
    path("api/chats/", views.list_my_chats, name="list_my_chats"),  # lista do usuário
    
    path("api/chats/create_or_get/", views.create_or_get_private_chat, name="create_or_get_private_chat"),
    
    path("api/chats/<str:chat_id>/messages/", views.chat_messages, name="chat_messages"),
    
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [ path("__reload__/", include("django_browser_reload.urls")), ]
