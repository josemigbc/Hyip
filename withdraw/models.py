from typing import Iterable, Optional
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()
# Create your models here.
class WithdrawRequest(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_approved = models.CharField(max_length=50,choices=[('P','Processing'),('R','Rejected'),('A','Accepted')],default='P')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = _("WithdrawRequest")
        verbose_name_plural = _("WithdrawRequests")
    
    def approve(self):
        self.is_approved = "A"
        self.save()
        
    def save(self,force_insert=False,force_update=False,*args,**kwargs):
        if not self.amount or not self.user:
            raise ValidationError(_("The amount and user must be given"))
        if self.amount > self.user.balance:
            raise ValidationError(_("The amount must be greater than user`s balance"))
        
        self.user.balance -= self.amount
        self.user.save()
        
        return super(WithdrawRequest,self).save(force_insert,force_update,*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.user}<{self.amount}>"
    

