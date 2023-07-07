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
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = _("WithdrawRequest")
        verbose_name_plural = _("WithdrawRequests")
    
    """ def clean(self):
        if self.amount >= self.user.balance:
            raise ValidationError(_("The amount must be greater than user`s balance")) """
    
    def approve(self):
        self.is_approved = True
        self.save()
    

