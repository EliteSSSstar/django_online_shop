
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

class StoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.manager = User.objects.create_user(username='manager', password='managerpass', is_superuser=True)

    def test_valid_login(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)

    def test_invalid_login(self):
        User.objects.create_user(username='testuser', password='testpass')
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpass'})
        self.assertContains(response, 'Invalid username or password')

    def test_registration_success(self):
        response = self.client.post('/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'pass1234',
            'password2': 'pass1234'
        })
        self.assertEqual(response.status_code, 302)

    def test_registration_password_mismatch(self):
        response = self.client.post('/register/', {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password1': 'pass1234',
            'password2': 'wrongpass'
        })
        self.assertContains(response, 'Passwords do not match.')

    def test_manager_creates_staff(self):
        self.client.login(username='manager', password='managerpass')
        response = self.client.post('/create_staff/', {
            'username': 'staffuser',
            'email': 'staff@example.com',
            'password': 'staffpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='staffuser').exists())