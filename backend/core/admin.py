from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ScanRecord

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        ('WasteWise Role', {'fields': ('role',)}),
    )

@admin.register(ScanRecord)
class ScanRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_class', 'confidence_score', 'created_at')
    list_filter = ('predicted_class', 'created_at')
    search_fields = ('user__username',)