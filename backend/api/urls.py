from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views.jwt import CustomTokenObtainPairView
from .views.user import Register

urlpatterns = [
    path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register', Register.as_view(), name='register')
]
