from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class DepositRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def approve(self):
        self.is_approved = True
        self.save()