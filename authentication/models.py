from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserManager(BaseUserManager):
    
    def create_user(self,username,email,password,**extra_fields):
        if not username or not email:
            raise ValueError(_("Username and Email should be set"))
        
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username,email,password,**extra_fields):
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(username,email,password,**extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(_("email address"),unique=True, max_length=254)
    wallet = models.TextField(null=True,blank=True)
    balance = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    
    REQUIRED_FIELDS = ['email']
    
    USERNAME_FIELD = 'username'
    
    objects = UserManager()
    
class Refferal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name="user")
    refferal_of = models.ForeignKey(User,on_delete=models.CASCADE, related_name="refferal_of",null=True,blank=True)