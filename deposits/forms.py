from django.forms import ModelForm
from .models import DepositRequest

class DepositRequestForm(ModelForm):
    
    class Meta:
        model = DepositRequest
        fields = ['user','amount']