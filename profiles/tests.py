from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile

class UserProfileAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user-profiles')

    def test_create_user_profile(self):
        image = SimpleUploadedFile("profile.jpg", b"file_content", "image/png")
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'bio': 'Hello, I am John Doe.',
            'profile_picture': image
        }

        response = self.client.post(self.url, data, format='multipart')

        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().name, 'John Doe')

    def test_update_user_profile(self):
        user_profile = UserProfile.objects.create(
            name='Ram',
            email='ram@example.com',
            bio='Hello, I am Ram.'
        )

        update_url = reverse('user-profile-detail', kwargs={'pk': user_profile.pk})
        image = SimpleUploadedFile("profile.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'name': 'Ravi',
            'email': 'Ravi@example.com',
            'bio': 'Hello, I am ravi.',
            'profile_picture': image
        }

        response = self.client.patch(update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get().name, 'Jane Doe')
        self.assertEqual(UserProfile.objects.get().email, 'janedoe@example.com')

    image = SimpleUploadedFile("profile.jpg", b"file_content", content_type="image/jpeg")
    def test_invalid_user_profile(self):
        image = SimpleUploadedFile("profile.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'name': 'John Doe',
            'email': 'invalidemail',
            'bio': 'Hello, I am John Doe.',
            'profile_picture': image
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserProfile.objects.count(), 0)
