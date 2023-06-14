from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/')

    def __str__(self):
        return self.email
