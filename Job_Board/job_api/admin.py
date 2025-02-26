from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'mobile_number', 'is_staff', 'is_verified')
    search_fields = ('email', 'username', 'mobile_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'mobile_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'mobile_number', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_verified')}
        ),
    )

# Register the custom User model with the customized admin panel
admin.site.register(User, CustomUserAdmin)
