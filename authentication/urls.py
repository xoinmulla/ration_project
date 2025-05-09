# authentication/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # next_page can be set in settings.LOGOUT_REDIRECT_URL

    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='authentication/password_reset_form.html',
                                              email_template_name='authentication/password_reset_email.html',
                                              subject_template_name='authentication/password_reset_subject.txt'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
         name='password_reset_complete'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]