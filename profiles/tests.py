from django.contrib.auth.models import User, Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile
from io import BytesIO
from PIL import Image

class UserProfileAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        permission = Permission.objects.get(codename='change_userprofile')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(user=self.user)
        self.url = reverse('user-profiles')


    def test_create_user_profile(self):
        f = BytesIO()
        image = Image.new("RGB", (100, 100))
        image.save(f, 'png')
        f.seek(0)
        image = SimpleUploadedFile("profile.jpg", content = f.read() ,)
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
        f = BytesIO()
        t_image = Image.new("RGB", (100, 100))
        t_image.save(f, 'png')
        f.seek(0)
        image = SimpleUploadedFile("profile.jpg", content = f.read() ,)

        user_profile = UserProfile.objects.create(
            name='Ram',
            email='ram@example.com',
            bio='Hello, I am Ram.',
            profile_picture = image
        )

        update_url = reverse('user-profile-detail', kwargs={'pk': user_profile.pk})
        
        data = {
            'name': 'Ravi',
            'email': 'Ravi@example.com',
            'bio': 'Hello, I am ravi.',
            'profile_picture': image
        }

        response = self.client.patch(update_url, data, format='multipart')

        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get().name, 'Ravi')
        self.assertEqual(UserProfile.objects.get().email, 'Ravi@example.com')

    def test_invalid_user_profile(self):
        f = BytesIO()
        image = Image.new("RGB", (100, 100))
        image.save(f, 'png')
        f.seek(0)
        image = SimpleUploadedFile("profile.jpg", content = f.read() ,)
        data = {
            'name': 'John Doe',
            'email': 'invalidemail',
            'bio': 'Hello, I am John Doe.',
            'profile_picture': image
        }

        response = self.client.post(self.url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserProfile.objects.count(), 0)
