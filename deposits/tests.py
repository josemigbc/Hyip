from django.test import TestCase
from .models import DepositRequest
from .forms import DepositChangeState
from django.conf import settings
from django.contrib.auth import get_user_model
from unittest.mock import patch,Mock

User = get_user_model()

# Create your tests here.
class DepositRequestTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test",balance=2000)
    
    def test_create_deposit_request(self):
        deposit_request = DepositRequest.objects.create(user=self.user,amount=1000)
        self.assertEqual(deposit_request.user,self.user)
        self.assertEqual(deposit_request.amount,1000)
        self.assertEqual(deposit_request.is_approved,"P")
        
        with self.assertRaises(Exception):
            DepositRequest.objects.create(user=self.user)
        
        with self.assertRaises(Exception):
            DepositRequest.objects.create(amount=1000)
        
        with self.assertRaises(Exception):
            DepositRequest.objects.create()
            
    def test_approve(self):
        deposit_request = DepositRequest.objects.create(user=self.user,amount=1000)
        deposit_request.approve()
        self.assertEqual(deposit_request.is_approved,"A")
        self.assertEqual(self.user.balance,3000)
        
class DepositViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test")
    
    def test_get(self):
        response = self.client.get("/deposit/")
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        
        self.client.login(username="test",password="test")
        response = self.client.get("/deposit/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Amount")
        
    def test_post(self):
        
        response = self.client.post("/deposit/")
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        deposit_request = DepositRequest.objects.all().first()
        self.assertIsNone(deposit_request)
        
        response = self.client.post("/deposit/",{"amount":1000})
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        deposit_request = DepositRequest.objects.all().first()
        self.assertIsNone(deposit_request)
        
        self.client.login(username="test",password="test")
        response = self.client.post("/deposit/",{"amount":1000})
        deposit_request = DepositRequest.objects.all().first()
        self.assertEqual(response.status_code,302)
        self.assertEqual(deposit_request.user,self.user)
        self.assertEqual(deposit_request.amount,1000)
        self.assertEqual(deposit_request.is_approved,"P")
        
        response = self.client.post("/deposit/")
        self.assertEqual(response.status_code,200)
        deposit_request = DepositRequest.objects.all().last()
        self.assertEqual(deposit_request.user,self.user)
        self.assertEqual(deposit_request.amount,1000)
        self.assertEqual(deposit_request.is_approved,"P")
        
class DepositChangeStateTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(username="test",email="test@test.com",password="testing1234",balance=3000)
        cls.deposit = DepositRequest.objects.create(user=user,amount=1000)
    
    def test_is_valid_with_ok(self):
        form = DepositChangeState({"approved": "R"},instance=self.deposit)
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
    
    def test_is_valid_with_ok(self):
        self.deposit.is_approved = "A"
        form = DepositChangeState({"approved": "R"},instance=self.deposit)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)
    
    @patch.object(DepositRequest,"approve")
    def test_save_with_A(self,mock:Mock):
        form = DepositChangeState({"approved": "A"},instance=self.deposit)
        is_valid = form.is_valid()
        form.save()
        mock.assert_called_once()
        self.assertTrue(is_valid)
    
    @patch.object(DepositRequest,"approve")
    def test_save_with_R(self,mock:Mock):
        form = DepositChangeState({"approved": "R"},instance=self.deposit)
        is_valid = form.is_valid()
        form.save()
        mock.assert_not_called()
        self.assertTrue(is_valid)
        