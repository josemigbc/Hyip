from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.http.request import HttpRequest
from .models import WithdrawRequest
from .forms import WithDrawRequestForm,WithDrawChangeStateForm

# Register your models here.
class WithdrawRequestAdmin(admin.ModelAdmin):
    form = WithDrawRequestForm
    readonly_fields = ('user','amount','is_approved','created')
    
    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        if obj:
            return WithDrawChangeStateForm
        return super().get_form(request, obj, change, **kwargs)
    
    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> List[str] | Tuple[Any, ...]:
        if not obj:
            return ()
        return super().get_readonly_fields(request, obj)
    
admin.site.register(WithdrawRequest,WithdrawRequestAdmin)