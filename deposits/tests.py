from django.test import TestCase
from .models import DepositRequest
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class DepositRequestTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test")
    
    def test_create_deposit_request(self):
        deposit_request = DepositRequest.objects.create(user=self.user,amount=1000)
        self.assertEqual(deposit_request.user,self.user)
        self.assertEqual(deposit_request.amount,1000)
        self.assertFalse(deposit_request.is_approved)
        
        with self.assertRaises(Exception):
            DepositRequest.objects.create(user=self.user)
        
        with self.assertRaises(Exception):
            DepositRequest.objects.create(amount=1000)
        
        with self.assertRaises(Exception):
            DepositRequest.objects.create()
            
    def test_approve(self):
        deposit_request = DepositRequest.objects.create(user=self.user,amount=1000)
        deposit_request.approve()
        self.assertTrue(deposit_request.is_approved)
        
class DepositViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test")
    
    def test_get(self):
        response = self.client.get("/deposit/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Amount")
        
    def test_post(self):
        
        response = self.client.post("/deposit/")
        self.assertEqual(response.status_code,200)
        deposit_request = DepositRequest.objects.all().first()
        self.assertIsNone(deposit_request)
        
        response = self.client.post("/deposit/",{"amount":1000})
        self.assertEqual(response.status_code,200)
        deposit_request = DepositRequest.objects.all().first()
        self.assertIsNone(deposit_request)
        
        self.client.login(username="test",password="test")
        response = self.client.post("/deposit/",{"amount":1000})
        deposit_request = DepositRequest.objects.all().first()
        self.assertEqual(response.status_code,302)
        self.assertEqual(deposit_request.user,self.user)
        self.assertEqual(deposit_request.amount,1000)
        self.assertFalse(deposit_request.is_approved)
        
        response = self.client.post("/deposit/")
        self.assertEqual(response.status_code,200)
        deposit_request = DepositRequest.objects.all().last()
        self.assertEqual(deposit_request.user,self.user)
        self.assertEqual(deposit_request.amount,1000)
        self.assertFalse(deposit_request.is_approved)