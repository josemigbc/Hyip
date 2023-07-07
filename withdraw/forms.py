from django.forms import ModelForm
from .models import WithdrawRequest

class WithDrawRequestForm(ModelForm):
    class Meta:
        model = WithdrawRequest
        fields = ["user","amount"]