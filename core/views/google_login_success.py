from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken

@login_required
def google_login_success(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    frontend_url = "http://localhost:5173/social/callback"
    return redirect(f"{frontend_url}?access={access_token}&refresh={refresh_token}")
