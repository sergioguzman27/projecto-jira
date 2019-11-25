""" Urls de los reportes """

# Django
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from myapps.reports.views import ReportsViews

router = DefaultRouter()
router.register(r'reports', ReportsViews, basename='reports')

urlpatterns = [
  path('', include(router.urls))
]