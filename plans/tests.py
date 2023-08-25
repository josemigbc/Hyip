from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Plan
from .forms import PlanForm
from authentication.models import Refferal
import datetime
from freezegun import freeze_time

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

    @freeze_time("2023-08-24 12:00")
    def test_daily_payment_with_no_last_paid_spent_time_one_day(self):
        plan = Plan.objects.create(user=self.user,amount=30)
        with freeze_time("2023-08-25 12:01"):
            amount = plan.daily_payment()
        self.assertEqual(amount,0.3)
        self.assertEqual(self.user.balance,2970.3)
    
    @freeze_time("2023-08-24 12:00")
    def test_daily_payment_with_no_last_paid_spent_time_gt_one(self):
        plan = Plan.objects.create(user=self.user,amount=30)
        with freeze_time("2023-08-27 12:01"):
            amount = plan.daily_payment()
        self.assertEqual(amount,0.9)
        self.assertEqual(self.user.balance,2970.9)
    
    @freeze_time("2023-08-24 12:00")
    def test_daily_payment_with_no_last_paid_spent_time_lt_one_same_day(self):
        plan = Plan.objects.create(user=self.user,amount=30)
        with freeze_time("2023-08-24 23:00"):
            amount = plan.daily_payment()
        self.assertIsNone(amount)
        self.assertEqual(self.user.balance,2970)
    
    @freeze_time("2023-08-24 12:00")
    def test_daily_payment_with_no_last_paid_spent_time_lt_one_next_date(self):
        plan = Plan.objects.create(user=self.user,amount=30)
        with freeze_time("2023-08-25 11:59"):
            amount = plan.daily_payment()
        self.assertEqual(amount,0)
        self.assertEqual(self.user.balance,2970)
    
    @freeze_time("2023-08-24 12:00")
    def test_daily_payment_with_last_paid_spent_time_one_day(self):
        plan = Plan.objects.create(user=self.user,amount=30)
        with freeze_time("2023-08-26 12:01"):
            plan.last_paid = plan.created.date() + datetime.timedelta(days=1)
            amount = plan.daily_payment()
        self.assertEqual(amount,0.3)
        self.assertEqual(self.user.balance,2970.3)
    
    @freeze_time("2023-08-24 12:00")
    def test_daily_payment_with_last_paid_spent_time_gt_one(self):
        plan = Plan.objects.create(user=self.user,amount=30)
        with freeze_time("2023-08-28 12:01"):
            plan.last_paid = plan.created.date() + datetime.timedelta(days=1)
            amount = plan.daily_payment()
        self.assertEqual(amount,0.9)
        self.assertEqual(self.user.balance,2970.9)
    
    @freeze_time("2023-08-24 12:00")
    def test_daily_payment_with_last_paid_spent_time_lt_one_same_day(self):
        plan = Plan.objects.create(user=self.user,amount=30)
        with freeze_time("2023-08-25 23:00"):
            plan.last_paid = plan.created.date() + datetime.timedelta(days=1)
            amount = plan.daily_payment()
        self.assertIsNone(amount)
        self.assertEqual(self.user.balance,2970)
    
    @freeze_time("2023-08-24 12:00")
    def test_daily_payment_with_no_last_paid_spent_time_lt_one_next_date(self):
        plan = Plan.objects.create(user=self.user,amount=30)
        with freeze_time("2023-08-26 11:59"):
            plan.last_paid = plan.created.date() + datetime.timedelta(days=1)
            amount = plan.daily_payment()
        self.assertEqual(amount,0)
        self.assertEqual(self.user.balance,2970)
        
    def test_save(self):
        plan = Plan.objects.create(user=self.user,amount=200)
        self.assertEqual(self.user.balance,2800)
        
        plan.last_paid = timezone.now()
        plan.save()
        self.assertEqual(self.user.balance,2800)

class PlanViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test",balance=3000)
        
    def test_get(self):
        response = self.client.get("/plan/")
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        
        self.client.login(username="test",password="test")
        response = self.client.get("/plan/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Amount")
        
    def test_post(self):
        response = self.client.post("/plan/")
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        
        response = self.client.post("/plan/",{"amount":1000})
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        
        self.client.login(username="test",password="test")
        response = self.client.post("/plan/",{"amount":1000})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url,"/")
        
        plan = Plan.objects.filter(user=self.user).first()
        self.assertIsNotNone(plan)
        self.assertEqual(User.objects.get(username="test").balance,2000)
        
        response = self.client.post("/plan/")
        self.assertEqual(response.status_code,200)
        
        response = self.client.post("/plan/",{"amount":3000})
        self.assertEqual(response.status_code,200)
        plan = Plan.objects.filter(user=self.user).last()
        self.assertEqual(plan.amount,1000)
        self.assertEqual(User.objects.get(username="test").balance,2000)
        
class RefferalSystemTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test")
        self.refferal = User.objects.create_user(username="testref",email="testref@test.com",password="test",balance=3000,refferal_of=self.user.pk)
        
    def test_pay_commision(self):
        Plan.objects.create(user=self.refferal,amount=1000)
        self.assertEqual(User.objects.get(pk=self.user.pk).balance,100)
        self.assertEqual(User.objects.get(pk=self.refferal.pk).balance,2000)
        
class PlanFormTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test",email="test@test.com",password="testing1234",balance=3000)
    
    def test_is_valid_with_none(self):
        form = PlanForm({})
        is_valid = form.is_valid()
        self.assertFalse(is_valid)
    
    def test_is_valid_with_amount_lt_balance(self):
        form = PlanForm({"user":self.user, "amount": 2000})
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
    
    def test_is_valid_with_amount_gt_balance(self):
        form = PlanForm({"user":self.user, "amount": 4000})
        is_valid = form.is_valid()
        self.assertFalse(is_valid)
    
    def test_is_valid_with_amount_eq_balance(self):
        form = PlanForm({"user":self.user, "amount": 3000})
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
    