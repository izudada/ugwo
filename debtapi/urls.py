from django.urls import include, path
from rest_framework.routers import DefaultRouter

from debtapi.views import DebtViewSet


router = DefaultRouter()
router.register(r'debt', DebtViewSet, basename='debt')  

urlpatterns = [path('', include(router.urls))]
