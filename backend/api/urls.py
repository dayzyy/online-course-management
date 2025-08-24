from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from .views.jwt import CustomTokenObtainPairView
from .views.user import Register
from .views.course import CourseViewSet
from .views.lecture import LectureViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lectures', LectureViewSet, basename='lecture')

urlpatterns = [
    path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    path('user/register', Register.as_view(), name='register'),

    path('', include(router.urls)),
]
