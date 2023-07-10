from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from .forms import UserRegistrationForm,UserChangeFrom
from .models import Refferal

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    form = UserRegistrationForm
    readonly_fields = ('username','email','created','last_login','is_staff','is_superuser')
    list_display = ('username','email','is_staff','is_superuser')
    
    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        if obj:
            return UserChangeFrom
        return super().get_form(request, obj, change, **kwargs)
    
    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> List[str] | Tuple[Any, ...]:
        if not obj:
            return ()
        return super().get_readonly_fields(request, obj)

    
admin.site.register(get_user_model(),CustomUserAdmin)
admin.site.register(Refferal)