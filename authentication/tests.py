from django.test import TestCase
from .models import User,Refferal
from django.db import IntegrityError

# Create your tests here.

class UserTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user("test","test@test.com","test")
        self.assertEqual(user.username,"test")
        self.assertEqual(user.email,"test@test.com")
        
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
            pass
        
        
        