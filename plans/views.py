from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import PlanForm
from .models import Plan

# Create your views here.
class PlanView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"plans/index.html")
    
    def post(self,request):
        try:
            Plan.objects.create(user=request.user,amount=request.POST.get("amount"))
            return redirect("/")
        except Exception as e:
            print(e)
        return self.get(request)
