from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialAccount

@csrf_exempt
def google_login_success(request):
    user = request.user

    if user.is_authenticated:
        # tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # tenta pegar info extra do Google
        social = SocialAccount.objects.filter(user=user).first()
        email = user.email or (social.extra_data.get("email") if social else "")
        avatar = social.get_avatar_url() if social else ""

        # redireciona pro front-end com tokens e dados
        frontend_url = "http://localhost:5173/social/callback"
        return redirect(
            f"{frontend_url}?access={access_token}&refresh={refresh_token}&email={email}&avatar={avatar}"
        )

    # fallback se não autenticado
    return redirect("http://localhost:5173/login")