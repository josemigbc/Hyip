from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Plan
from .forms import PlanForm

# Register your models here.
class PlanAdmin(admin.ModelAdmin):
    form = PlanForm
    readonly_fields = ("user","amount","created","last_paid")
    
    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> List[str] | Tuple[Any, ...]:
        if not obj:
            return ()
        return super().get_readonly_fields(request, obj)
    
admin.site.register(Plan,PlanAdmin)
