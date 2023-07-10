from typing import Any
from django.forms import ModelForm
from .models import Plan
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PlanForm(ModelForm):
    
    class Meta:
        model = Plan
        fields = ['user','amount']
        
    def is_valid(self) -> bool:
        if not self.data.get("amount")  or not self.data.get("user"):
            self.add_error(field="amount", error=ValidationError(_("The amount and user must be given")))
            return False
        if int(self.data.get("amount")) > self.data.get("user").balance:
            self.add_error(field="amount", error=ValidationError(_("The amount must not be greater than user`s balance")))
            return False 
        return super().is_valid()
