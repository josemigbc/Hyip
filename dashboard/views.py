from django.shortcuts import render
from authentication.models import Refferal
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    refferal = Refferal.objects.get(user=request.user)
    return render(request,"dashboard/index.html",context={"refferal":refferal})
