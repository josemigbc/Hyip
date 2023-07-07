from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
from .models import User,Refferal

# Create your views here.
class RegisterUserView(View):
    
    def get(self,request,pk=None):
        return render(request,"authentication/register.html")
    
    def post(self,request,pk=None):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data.get("username"))
            refferal_of = User.objects.filter(pk=pk).first()
            Refferal.objects.create(user=user,refferal_of=refferal_of)
            return redirect('/auth/login/')
        
        return render(request,"authentication/register.html")