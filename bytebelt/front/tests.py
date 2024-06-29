import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.api_base_url = 'http://localhost:8000/api/'  
        self.token = 'fake-token'
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.session['token'] = self.token
        self.client.session.save()
        
    @patch('requests.post')
    @patch('requests.get')
    def test_home_view(self, mock_get, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'id': self.user.id,
            'username': self.user.username,
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'id': 1, 'username': 'user1'},
            {'id': 2, 'username': 'user2'}
        ]

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')