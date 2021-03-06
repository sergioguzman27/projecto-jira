""" Urls del usuario """

# Django
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from myapps.users.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
  path('', include(router.urls))
]

