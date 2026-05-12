from django.urls import include, path
from rest_framework.routers import DefaultRouter

from authentication.views import AuthenticationViewSet


router = DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='auth')  

urlpatterns = [
    path('', include(router.urls)),
]
