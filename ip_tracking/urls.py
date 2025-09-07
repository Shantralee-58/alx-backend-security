from django.urls import path
from . import views

urlpatterns = [
    path('sensitive/', views.sensitive_view, name='sensitive'),
    path('test/', views.test_view, name='test'),
]

