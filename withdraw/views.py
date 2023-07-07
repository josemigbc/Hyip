from django.shortcuts import render,redirect
from django.views import View
from .forms import WithDrawRequestForm

# Create your views here.
class WithdrawRequestView(View):
    
    def get(self,request):
        return render(request,"withdraw/index.html")
    
    def post(self,request):
    
        data = {
            "user": request.user,
            "amount": request.POST.get("amount"),
        }
        form =  WithDrawRequestForm(data)
        if form.is_valid():
            form.save()
            return redirect("/")
        return self.get(request)