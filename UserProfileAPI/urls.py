from django.urls import path
from profiles.views import UserProfileAPIView

urlpatterns = [
    path('api/profiles/', UserProfileAPIView.as_view(), name='user-profiles'),
    path('api/profiles/<int:pk>/', UserProfileAPIView.as_view(), name='user-profile-detail'),
]
