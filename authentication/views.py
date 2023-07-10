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
            form.save(refferal_of=pk)
            return redirect('/auth/login/')
        
        return render(request,"authentication/register.html")