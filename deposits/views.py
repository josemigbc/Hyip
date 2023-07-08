from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import DepositRequestForm
# Create your views here.
class DepositView(LoginRequiredMixin, View):
    def get(self,request):
        return render(request,"deposit/index.html")
    
    def post(self,request):
        data = {
            "user": request.user,
            "amount": request.POST.get("amount")
        }
        form = DepositRequestForm(data)
        if form.is_valid():
            form.save()
            return redirect("/")
        return self.get(request)
            
