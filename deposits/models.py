from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class DepositRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_approved = models.CharField(max_length=50,choices=[('P','Processing'),('R','Rejected'),('A','Accepted')],default='P')
    created = models.DateTimeField(auto_now_add=True)
    
    def approve(self):
        self.is_approved = 'A'
        self.user.balance += self.amount
        self.user.save()
        
    def __str__(self) -> str:
        return f"{self.user} <{self.amount}>"