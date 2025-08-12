from django.contrib import admin
from .models import Product,CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Product)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)