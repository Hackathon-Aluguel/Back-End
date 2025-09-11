from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def google_login_success(request):
    user = request.user
    if user.is_authenticated:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        frontend_url = "http://localhost:5173/social/callback"
        return redirect(f"{frontend_url}?access={access_token}&refresh={refresh_token}")
    else:
        return redirect("http://localhost:5173/login")
