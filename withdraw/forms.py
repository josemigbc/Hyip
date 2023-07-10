from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from typing import Any
from django.forms import ModelForm,ChoiceField
from .models import WithdrawRequest

class WithDrawRequestForm(ModelForm):
    class Meta:
        model = WithdrawRequest
        fields = ["user","amount"]
        
class WithDrawChangeStateForm(ModelForm):
    
    approved = ChoiceField(choices=[('R','Rejected'),('A','Accepted')])
    class Meta:
        model = WithdrawRequest
        fields = ()
        
    def is_valid(self) -> bool:
        if self.instance.is_approved != 'P':
            self.add_error('approved',ValidationError(_("The field should be Processing to modify it")))
            return False
        return super().is_valid()
    
    def save(self, commit: bool = ...) -> Any:
        if self.cleaned_data["approved"] == "A":
            self.instance.approve()
        self.instance.is_approved = "R"
        self.instance.save()
        return super().save(commit)