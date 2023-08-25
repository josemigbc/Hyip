from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import WithdrawRequest
from .forms import WithDrawChangeStateForm
from unittest.mock import patch,Mock

User = get_user_model()

# Create your tests here.
class WithdrawRequestTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test",balance=2000)
    
    def test_create_withdraw_request(self):
        withdraw_request = WithdrawRequest.objects.create(user=self.user,amount=1000)
        self.assertEqual(withdraw_request.user,self.user)
        self.assertEqual(withdraw_request.amount,1000)
        self.assertEqual(withdraw_request.is_approved,"P")
        self.assertEqual(self.user.balance,1000)
        
        with self.assertRaises(Exception):
            WithdrawRequest.objects.create(user=self.user,amount=3000)
        
        with self.assertRaises(Exception):
            WithdrawRequest.objects.create(user=self.user)
        
        with self.assertRaises(Exception):
            WithdrawRequest.objects.create(amount=1000)
        
        with self.assertRaises(Exception):
            WithdrawRequest.objects.create()
            
    def test_approve(self):
        withdraw_request = WithdrawRequest.objects.create(user=self.user,amount=1000)
        withdraw_request.approve()
        self.assertEqual(withdraw_request.is_approved,"A")
        
class WithdrawViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test",balance=2000)
    
    def test_get(self):
        response = self.client.get("/withdraw/")
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        
        self.client.login(username="test",password="test")
        response = self.client.get("/withdraw/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Amount")
        
    def test_post(self):
        
        response = self.client.post("/withdraw/")
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        withdraw_request = WithdrawRequest.objects.all().first()
        self.assertIsNone(withdraw_request)
        
        response = self.client.post("/withdraw/",{"amount":1000})
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        withdraw_request = WithdrawRequest.objects.all().first()
        self.assertIsNone(withdraw_request)
        
        self.client.login(username="test",password="test")
        response = self.client.post("/withdraw/",{"amount":1000})
        withdraw_request = WithdrawRequest.objects.all().first()
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url,"/")
        self.assertEqual(withdraw_request.user,self.user)
        self.assertEqual(withdraw_request.amount,1000)
        self.assertEqual(withdraw_request.is_approved,"P")
        self.assertEqual(User.objects.get(pk=self.user.pk).balance,1000)
        
        response = self.client.post("/withdraw/")
        self.assertEqual(response.status_code,200)
        withdraw_request = WithdrawRequest.objects.all().last()
        self.assertEqual(withdraw_request.user,self.user)
        self.assertEqual(withdraw_request.amount,1000)
        self.assertEqual(withdraw_request.is_approved,"P")
        
        response = self.client.post("/withdraw/",{"amount": 3000})
        self.assertEqual(response.status_code,200)
        withdraw_request = WithdrawRequest.objects.all().last()
        self.assertEqual(withdraw_request.user,self.user)
        self.assertEqual(withdraw_request.amount,1000)
        self.assertEqual(withdraw_request.is_approved,"P")
        
class WithdrawChangeStateTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(username="test",email="test@test.com",password="testing1234",balance=3000)
        cls.deposit = WithdrawRequest.objects.create(user=user,amount=1000)
    
    def test_is_valid_with_ok(self):
        form = WithDrawChangeStateForm({"approved": "R"},instance=self.deposit)
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
    
    def test_is_valid_with_ok(self):
        self.deposit.is_approved = "A"
        form = WithDrawChangeStateForm({"approved": "R"},instance=self.deposit)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)
    
    @patch.object(WithdrawRequest,"approve")
    def test_save_with_A(self,mock:Mock):
        form = WithDrawChangeStateForm({"approved": "A"},instance=self.deposit)
        is_valid = form.is_valid()
        form.save()
        mock.assert_called_once()
        self.assertTrue(is_valid)
    
    @patch.object(WithdrawRequest,"approve")
    def test_save_with_R(self,mock:Mock):
        form = WithDrawChangeStateForm({"approved": "R"},instance=self.deposit)
        is_valid = form.is_valid()
        form.save()
        mock.assert_not_called()
        self.assertTrue(is_valid)