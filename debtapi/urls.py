from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from debtapi.views import DebtViewSet


router = DefaultRouter()
router.register(r'debt', DebtViewSet, basename='debt')  

urlpatterns = [
    path('', include(router.urls)),

    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),

]
