from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Plan
import datetime

User = get_user_model()

# Create your tests here.
class PlanTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test",balance=3000)
    
    def test_create(self):
        Plan.objects.create(user=self.user,amount=2000)
        plan = Plan.objects.filter(user=self.user).first()
        self.assertEqual(plan.amount,2000)
        self.assertEqual(self.user.balance,1000)
        
        with self.assertRaises(Exception):
            Plan.objects.create(user=self.user,amount=2000)
        
        with self.assertRaises(Exception):
            Plan.objects.create(user=self.user)
            
        with self.assertRaises(Exception):
            Plan.objects.create(amount=500)
            
        with self.assertRaises(Exception):
            Plan.objects.create()
            
    def test_daily_earning(self):
        plan = Plan.objects.create(user=self.user,amount=200)
        self.assertEqual(plan.daily_earning,0.02)
        
        plan = Plan.objects.create(user=self.user,amount=80)
        self.assertEqual(plan.daily_earning,0.01)
        
    def test_total_earning(self):
        plan = Plan.objects.create(user=self.user,amount=200)
        plan.last_paid = plan.created + datetime.timedelta(days=5)
        self.assertEqual(plan.total_earning,0.02*5*plan.amount)
        
        plan.last_paid = plan.created + datetime.timedelta(days=5,hours=10)
        self.assertEqual(plan.total_earning,0.02*5*plan.amount)
        
        plan = Plan.objects.create(user=self.user,amount=80)
        plan.last_paid = plan.created + datetime.timedelta(days=5)
        self.assertEqual(plan.total_earning,0.01*5*plan.amount)
        
        plan.last_paid = plan.created + datetime.timedelta(days=5,hours=10)
        self.assertEqual(plan.total_earning,0.01*5*plan.amount)
        
    def test_save(self):
        plan = Plan.objects.create(user=self.user,amount=200)
        self.assertEqual(self.user.balance,2800)
        
        plan.last_paid = timezone.now()
        plan.save()
        self.assertEqual(self.user.balance,2800)
        