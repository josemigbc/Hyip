from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from authentication.models import Refferal

User = get_user_model()

# Create your models here.
class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    last_paid = models.DateField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def daily_earning(self):
        if self.amount < 100:
            return 0.01
        return 0.02
    
    @property
    def total_earning(self):
        time = self.last_paid - self.created
        return self.daily_earning*time.days*self.amount
    
    def daily_payment(self):
        payment_time = self.created.time()
        if not self.last_paid:
            self.last_paid = self.created.date()
        now = timezone.now()
        spent_time = now.date() - self.last_paid
        amount = 0
        if spent_time.days < 1:
            return None
        if spent_time.days >= 1:
            amount += self.daily_earning*self.amount*(spent_time.days - 1)
            if now.time() > payment_time:
                amount += self.daily_earning*self.amount

        amount = round(amount,1)
        self.user.balance += amount
        self.last_paid = now.date()
        self.user.save()
        return amount
    
    def save(self,force_insert=False,force_update=False,*args,**kwargs):
        
        if not self.amount or not self.user:
            raise ValidationError(_("The amount and user must be given"))
        if not self.pk:
            if int(self.amount) > self.user.balance:
                raise ValidationError(_("The amount must not be greater than user`s balance"))
        
            self.user.balance -= int(self.amount)
            self.user.save()
            refferal = Refferal.objects.get(user=self.user)
            if refferal.refferal_of:
                refferal.refferal_of.balance += 0.1*self.amount
                refferal.refferal_of.save()
        
        return super(Plan,self).save(force_insert,force_update,*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.user}<{self.amount}>"