from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm

# Create your views here.
class RegisterUserView(View):
    
    def get(self,request):
        return render(request,"authentication/register.html")
    
    def post(self,request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/auth/login/')
        
        return render(request,"authentication/register.html")