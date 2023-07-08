from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.exceptions import ValidationError
from .forms import WithDrawRequestForm

# Create your views here.
class WithdrawRequestView(LoginRequiredMixin,View):
    
    def get(self,request):
        return render(request,"withdraw/index.html")
    
    def post(self,request):
    
        data = {
            "user": request.user,
            "amount": request.POST.get("amount"),
        }
        form =  WithDrawRequestForm(data)
        if form.is_valid():
            try:
                form.save()
                return redirect("/")
            except ValidationError:
                pass
        return self.get(request)