from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', LoginView.as_view(), name="login_view"),
    path('register/', RegisterView.as_view(), name="register_view"),
    path('logout/', LogoutView.as_view(), name="logout_view"),
    path('reset/password/', PassworReset.as_view(), name="password_reset_view"),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="users/email_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/reset.html"),
         name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/reset_done.html"),
         name='password_reset_complete'),
    path('profile/', UserProfileView.as_view(), name="user_profile_view"),
    path('settings/', UsersSetting.as_view(), name="user_settings_view"),
    path('reset/username/', UsernameResetView.as_view(),
         name='username_reset_view'),
    path('reset/email/', EmailResetView.as_view(), name='email_reset_view'),
    path('reset/name/', PersonalNameView.as_view(), name='personal_reset_view'),
    path('reset/password/', PasswordResetView.as_view(),
         name='password_reset_view'),
]
