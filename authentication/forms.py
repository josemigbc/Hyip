from typing import Any
from django.contrib.auth.forms import UserCreationForm
from .models import User,Refferal
from django import forms

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','wallet','password1','password2']
        
    def save(self, commit: bool = ...,refferal_of=None) -> Any:
        response = super().save(commit=True)
        user = User.objects.get(username=self.cleaned_data["username"])
        refferal_of = User.objects.filter(pk=refferal_of).first() if refferal_of else None
        Refferal.objects.create(user=user,refferal_of=refferal_of)
        return response
        
class UserChangeFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ('wallet','balance')