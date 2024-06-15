from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegisterForm

class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    model = User
    list_display = ('email','is_staff','is_superuser')
    list_filter = ('email','is_staff','is_superuser')
    fieldsets = (
        (None, {'fields': ('first_name','last_name','username','email', 'password','picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','username','email','password1', 'password2','picture',
                       'is_staff','is_active',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)