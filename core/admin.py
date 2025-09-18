from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patient, HeartRate

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_doctor', 'is_staff', 'is_superuser')
    list_filter = ('is_doctor', 'is_staff', 'is_superuser', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_doctor', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_doctor')}
        ),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(HeartRate)
