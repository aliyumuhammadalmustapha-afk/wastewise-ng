from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
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
