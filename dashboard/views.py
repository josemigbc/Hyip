from django.shortcuts import render
from authentication.models import Refferal
from django.contrib.auth.decorators import login_required
from deposits.models import DepositRequest
from withdraw.models import WithdrawRequest
from plans.models import Plan

# Create your views here.
@login_required
def index(request):
    plans = Plan.objects.filter(user=request.user)
    for plan in plans:
        plan.daily_payment()
    refferal = Refferal.objects.get(user=request.user)
    return render(request,"dashboard/index.html",context={"refferal":refferal})

@login_required
def history(request):
    deposits = DepositRequest.objects.filter(user=request.user).order_by("-created")
    withdraws = WithdrawRequest.objects.filter(user=request.user).order_by("-created")
    plans = Plan.objects.filter(user=request.user).order_by("-created")
    context = {
        "deposits":deposits,
        "withdraws": withdraws,
        "plans": plans,
    }
    
    return render(request,"dashboard/history.html",context)