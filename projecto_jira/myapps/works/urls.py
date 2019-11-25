""" Urls de las tareas """

# Django
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from myapps.works.views import WorkViewSet

router = DefaultRouter()
router.register(r'works', WorkViewSet, basename='works')

urlpatterns = [
  path('', include(router.urls))
]