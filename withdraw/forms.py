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
    
    approved = ChoiceField(choices=[('A','Accepted'),('R','Rejected')])
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
        else:
            self.instance.is_approved = "R"
            self.instance.save()
            self.instance.user.balance += self.instance.amount
            self.instance.user.save()
        return super().save(commit)