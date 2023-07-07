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
        
        with self.assertRaises(TypeError):
            DepositRequest.objects.create(user=self.user)
        
        with self.assertRaises(TypeError):
            DepositRequest.objects.create(amount=1000)
        
        with self.assertRaises(TypeError):
            DepositRequest.objects.create()
            
    def test_approve(self):
        deposit_request = DepositRequest.objects.create(user=self.user,amount=1000)
        deposit_request.approve()
        self.assertTrue(deposit_request.is_approved)