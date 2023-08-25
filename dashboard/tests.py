from django.test import TestCase
from django.contrib.auth import get_user_model
from plans.models import Plan
from unittest.mock import patch,Mock
from authentication.models import Refferal

User = get_user_model()

# Create your tests here.
class DashboardViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test",email="test@test.com",password="testing1234",balance=3000)
        
    def setUp(self) -> None:
        self.client.login(username="test",password="testing1234")
    
    @patch.object(Plan,"daily_payment",)
    def test_index_with_no_plans(self,mock:Mock):
        self.client.login(username="test",password="testing1234")
        response = self.client.get("/")
        mock.assert_not_called()
        self.assertEqual(response.status_code,200)
        self.assertIn('refferal',response.context)
        
    @patch.object(Plan,"daily_payment",)
    def test_index_with_plans(self,mock:Mock):
        Plan.objects.create(user=self.user,amount=300)
        response = self.client.get("/")
        mock.assert_called_once()
        self.assertEqual(response.status_code,200)
        
    def test_history(self):
        response = self.client.get("/history/")
        self.assertEqual(response.status_code,200)
        self.assertIn('deposits',response.context)
        self.assertIn("withdraws",response.context)
        self.assertIn('plans',response.context)
