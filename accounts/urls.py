from django.urls import path
from .views import ForgotPasswordAPIView, ResetPasswordAPIView

urlpatterns = [
    path('auth/forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('auth/reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]