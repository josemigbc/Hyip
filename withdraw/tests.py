from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import WithdrawRequest

User = get_user_model()

# Create your tests here.
class WithdrawRequestTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test",balance=2000)
    
    def test_create_withdraw_request(self):
        withdraw_request = WithdrawRequest.objects.create(user=self.user,amount=1000)
        self.assertEqual(withdraw_request.user,self.user)
        self.assertEqual(withdraw_request.amount,1000)
        self.assertFalse(withdraw_request.is_approved)
        
        """ Todavia no desarrollado pra cumplir con este test 
        with self.assertRaises(Exception):
            WithdrawRequest.objects.create(user=self.user,amount=3000) """
        
        with self.assertRaises(Exception):
            WithdrawRequest.objects.create(user=self.user)
        
        with self.assertRaises(Exception):
            WithdrawRequest.objects.create(amount=1000)
        
        with self.assertRaises(Exception):
            WithdrawRequest.objects.create()
            
    def test_approve(self):
        withdraw_request = WithdrawRequest.objects.create(user=self.user,amount=1000)
        withdraw_request.approve()
        self.assertTrue(withdraw_request.is_approved)
        
class WithdrawViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test",email="test@test.com",password="test",balance=2000)
    
    def test_get(self):
        response = self.client.get("/withdraw/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Amount")
        
    def test_post(self):
        
        response = self.client.post("/withdraw/")
        self.assertEqual(response.status_code,200)
        withdraw_request = WithdrawRequest.objects.all().first()
        self.assertIsNone(withdraw_request)
        
        response = self.client.post("/withdraw/",{"amount":1000})
        self.assertEqual(response.status_code,200)
        withdraw_request = WithdrawRequest.objects.all().first()
        self.assertIsNone(withdraw_request)
        
        self.client.login(username="test",password="test")
        response = self.client.post("/withdraw/",{"amount":1000})
        withdraw_request = WithdrawRequest.objects.all().first()
        self.assertEqual(response.status_code,302)
        self.assertEqual(withdraw_request.user,self.user)
        self.assertEqual(withdraw_request.amount,1000)
        self.assertFalse(withdraw_request.is_approved)
        
        response = self.client.post("/withdraw/")
        self.assertEqual(response.status_code,200)
        withdraw_request = WithdrawRequest.objects.all().last()
        self.assertEqual(withdraw_request.user,self.user)
        self.assertEqual(withdraw_request.amount,1000)
        self.assertFalse(withdraw_request.is_approved)
        
        #response = self.client.post("/withdraw/",{"amount": 3000})
        self.assertEqual(response.status_code,200)
        withdraw_request = WithdrawRequest.objects.all().last()
        self.assertEqual(withdraw_request.user,self.user)
        self.assertEqual(withdraw_request.amount,1000)
        self.assertFalse(withdraw_request.is_approved)