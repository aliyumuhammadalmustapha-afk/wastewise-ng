from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password Reset flow
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        form_class=CustomPasswordResetForm,
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html',
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        form_class=CustomSetPasswordForm,
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html',
    ), name='password_reset_complete'),
    
    # AI Scanner routes
    path('scan/', views.scan_view, name='scan'),
    path('api/save-scan/', views.api_save_scan, name='api_save_scan'),
    path('scan/save/', views.save_scan_view, name='save_scan'),
    path('result/<int:scan_id>/', views.result_view, name='result'),
    
    # User & Admin Dashboards
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('history/', views.history_view, name='history'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('learn/', views.education_view, name='education'),
    path('about/', views.about_view, name='about'),
    path('api/classify/', views.classify_image, name='api_classify_image'),
]
