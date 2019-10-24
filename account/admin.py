from django.contrib import admin
from account.models import User, Note
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


class User_Admin(UserAdmin):
    fieldsets = (
        (None, {'fields': (
            'password', 'is_superuser')}),
        (('Personal info'),
         {'fields': ('email',)}),
        (('Important dates'),
         {'fields': ('last_login', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ['id', 'email', 'is_active', 'created_at']
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, User_Admin)
admin.site.register(Note)
admin.site.unregister(Group)
