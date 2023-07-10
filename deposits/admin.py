from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.http.request import HttpRequest
from .models import DepositRequest
from .forms import DepositRequestForm,DepositChangeState
# Register your models here.
class DepositRequestAdmin(admin.ModelAdmin):
    form = DepositRequestForm
    list_display = ('user','created')
    readonly_fields = ("user","amount","is_approved","created")
    
    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        if obj:
            return DepositChangeState
        return super().get_form(request, obj, change, **kwargs)
    
    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> List[str] | Tuple[Any, ...]:
        if not obj:
            return ()
        return super().get_readonly_fields(request, obj)


admin.site.register(DepositRequest,DepositRequestAdmin)
