from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    form = UserRegistrationForm
    fields = ('username','password','email','wallet','balance','created','last_login','is_staff','is_superuser')
    readonly_fields = ('username','password','email','created','last_login','is_staff','is_superuser')
    list_display = ('username','email','is_staff','is_superuser')

    
admin.site.register(get_user_model(),CustomUserAdmin)