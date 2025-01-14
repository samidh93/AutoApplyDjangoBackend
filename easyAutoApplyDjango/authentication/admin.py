from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

#admin.site.register(CustomUser, UserAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'wix_id', 'is_staff', 'is_active', 'date_joined')

admin.site.register(CustomUser, CustomUserAdmin)