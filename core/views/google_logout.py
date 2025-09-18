from django.contrib.auth import logout
from django.shortcuts import redirect

def google_logout(request):
    logout(request)  # remove sessão Django
    return redirect('http://localhost:5173/')  # ou sua home
