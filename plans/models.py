from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Create your models here.
class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    last_paid = models.DateTimeField(auto_now_add=True)
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
    
    def save(self,force_insert=False,force_update=False,*args,**kwargs):
        
        if not self.amount or not self.user:
            raise ValidationError(_("The amount and user must be given"))
        if int(self.amount) > self.user.balance:
            raise ValidationError(_("The amount must not be greater than user`s balance"))
        
        if not self.pk:
            self.user.balance -= int(self.amount)
            self.user.save()
        
        return super(Plan,self).save(force_insert,force_update,*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.user}<{self.amount}>"