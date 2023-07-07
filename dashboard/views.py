from django.shortcuts import render
from authentication.models import Refferal

# Create your views here.
def index(request):
    refferal = Refferal.objects.get(user=request.user)
    return render(request,"dashboard/index.html",context={"refferal":refferal})
