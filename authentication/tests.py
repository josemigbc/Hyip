from django.test import TestCase
from django.conf import settings
from .models import User,Refferal
from .forms import UserRegistrationForm
from django.db import IntegrityError

# Create your tests here.

class UserTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user("test","test@test.com","test")
        self.assertEqual(user.username,"test")
        self.assertEqual(user.email,"test@test.com")
        self.assertIsNotNone(Refferal.objects.get(user=user))
        
        with self.assertRaises(TypeError):
            User.objects.create_user()
        
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        
        with self.assertRaises(TypeError):
            User.objects.create_user(email="",username="")
        
        with self.assertRaises(ValueError):
            User.objects.create_user(email="",username="",password="test")
            
        with self.assertRaises(TypeError):
            User.objects.create_user(email="test2@test.com",username="test2")
        
        with self.assertRaises(TypeError):
            User.objects.create_user(username="")

        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="test",email="test2@test.com",password="test")
        
        with self.assertRaises(Exception):
            User.objects.create_user(email="test@test.com",username="test2",password="test")
            
    def test_create_superuser(self):
        user = User.objects.create_superuser("test","test@test.com","test")
        self.assertEqual(user.username,"test")
        self.assertEqual(user.email,"test@test.com")
        self.assertTrue(user.is_superuser)
        
class LoginViewTest(TestCase):
            
    def setUp(self):
        self.user = User.objects.create_user(username="test",email="test@test.com",password="testing1234")

    def test_get(self):
        response = self.client.get("/auth/login/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Username")
        self.assertContains(response,"Password")
                
    def test_post(self):
        data = {
            "username": "test",
            "password": "testing1234",
        }
        response = self.client.post("/auth/login/",data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url,"/")
                
        data = {
            "username": "test",
            "password": "testing",
        }
                
        response = self.client.post("/auth/login/",data)
        self.assertEqual(response.status_code,200)
                
        data = {
            "username": "test2",
            "password": "testing1234",
        }
                
        response = self.client.post("/auth/login/",data)
        self.assertEqual(response.status_code,200)

class RegisterUserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser",email="testuser@test.com",password="testing1234")
    
    def test_get(self):
        response = self.client.get("/auth/signup/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Username")
        self.assertContains(response,"Confirm Password")
        
    def test_post(self):
        data = {
            "username": "test",
            "email": "test@test.com",
            "password1": "testing1234",
            "password2": "testing1234",
        }
        
        response = self.client.post("/auth/signup/",data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url,settings.LOGIN_URL)
        user = User.objects.get(username="test")
        self.assertFalse(user.is_superuser)
        refferal_user = Refferal.objects.get(user=user)
        self.assertEqual(refferal_user.user,user)
        self.assertIsNone(refferal_user.refferal_of)
        
        data = {
            "username": "testuser2",
            "email": "testuser2@test.com",
            "password1": "testing1234",
            "password2": "testing1234",
        }
        response = self.client.post("/auth/signup/1/",data)
        self.assertEqual(response.status_code,302)
        user = User.objects.get(username="testuser2")
        self.assertFalse(user.is_superuser)
        refferal_user = Refferal.objects.get(user=user)
        self.assertEqual(refferal_user.user,user)
        self.assertEqual(refferal_user.refferal_of,User.objects.get(pk=1))
        
        data = {
            "username": "testuser3",
            "email": "testuser3@test.com",
            "password1": "testing1234",
            "password2": "testing1234",
        }
        response = self.client.post("/auth/signup/100/",data)
        self.assertEqual(response.status_code,302)
        user = User.objects.get(username="testuser3")
        refferal_user = Refferal.objects.get(user=user)
        
        self.assertEqual(refferal_user.user,user)
        self.assertIsNone(refferal_user.refferal_of)
        
        data = {
            "username": "test2",
            "email": "test2@test.com",
            "password1": "testing123",
            "password2": "testing1234",
        }
        response = self.client.post("/auth/signup/",data)
        self.assertEqual(response.status_code,200)
        
        data = {
            "username": "test2",
            "password1": "testing1234",
            "password2": "testing1234",
        }
        response = self.client.post("/auth/signup/",data)
        self.assertEqual(response.status_code,200)
        
        data = {
            "email": "test2@test.com",
            "password1": "testing123",
            "password2": "testing1234",
        }
        response = self.client.post("/auth/signup/",data)
        self.assertEqual(response.status_code,200)
        
        data = {
            "username": "testuser",
            "email": "testuser@test.com",
            "password1": "testing1234",
            "password2": "testing1234",
        }
        response = self.client.post("/auth/signup/",data)
        self.assertEqual(response.status_code,200)
        
        response = self.client.post("/auth/signup/",{})
        self.assertEqual(response.status_code,200)
        
class AuthenticatedViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",email="test@test.com",password="testing1234",balance=3000)
        
    def test_dashboard_view(self):
        
        response = self.client.get("/")
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        
        self.client.login(username="test",password="testing1234")
        response = self.client.get("/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"test")
            
    def deposit_withdraw_base(self,url):
        
        data = {"amount": 1000}
        
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
                
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        
        self.client.login(username="test",password="testing1234")
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Amount")
        
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,302)
        self.assertEqual("/",response.url)
        
    def test_deposit_view(self):
        self.deposit_withdraw_base("/deposit/")
    
    def test_withdraw_view(self):
        self.deposit_withdraw_base("/withdraw/")
        
class RegistrationFormTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.data = {
            "username": "test",
            "email": "test@test.com",
            "password1": "testing1234",
            "password2": "testing1234"
        }
    
    def test_save_with_no_refferal(self):
        form = UserRegistrationForm(self.data)
        is_valid = form.is_valid()
        form.save()
        user = User.objects.filter(username="test").last()
        refferal = Refferal.objects.filter(user=user).last()
        self.assertIsNotNone(user)
        self.assertIsNotNone(refferal)
        
    def test_save_with_refferal(self):
        refferal = User.objects.create_user(username="test2",email="test2@test.com",password="testing1234")
        form = UserRegistrationForm(self.data)
        is_valid = form.is_valid()
        form.save(refferal_of=refferal.id)
        user = User.objects.filter(username="test").last()
        refferal_obj = Refferal.objects.filter(user=user,refferal_of=refferal).last()
        self.assertIsNotNone(user)
        self.assertIsNotNone(refferal_obj)