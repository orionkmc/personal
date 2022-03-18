from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'type_user',
            'phone',
            'image',
            'qr',
        )}),

        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'type_user',
                'phone',
                'image',
                'password1',
                'password2'
            ),
        }),
    )
    list_display = ('qr_thumbnail', 'email', 'first_name', 'last_name', 'type_user',)
    search_fields = ('first_name', 'last_name', 'email',)
    list_filter = ('type_user', 'is_staff', 'is_active', 'is_superuser')
    ordering = ('email', )

admin.site.register(User, UserAdmin)
