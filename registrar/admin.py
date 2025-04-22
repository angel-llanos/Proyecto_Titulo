from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
