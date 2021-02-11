from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.models import SMSModel

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email',
        'username',
        'business_name',
        'date_joined',
        'last_login',
        'is_superuser'
    )
    date_hierarchy = 'date_joined'
    ordering = ('-date_joined', )

admin.site.register(SMSModel)
