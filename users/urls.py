from django.urls import path, include
from .views import LoginView, RegisterView, LogoutView, password_reset_request
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', LoginView.as_view(), name="login_view"),
    path('register/', RegisterView.as_view(), name="register_view"),
    path('logout/', LogoutView.as_view(), name="logout_view"),
    path('reset/password/', password_reset_request, name="password_reset_view"),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),




]
