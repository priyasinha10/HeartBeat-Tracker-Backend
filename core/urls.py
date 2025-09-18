from django.urls import path
from .views import UserRegisterView, CustomTokenObtainPairView, PatientListCreateView,HeartRateListCreateView, HeartRateDetailView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),

    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientListCreateView.as_view(), name='patient-detail'),
     path('heart_rates/', HeartRateListCreateView.as_view(), name='heart-rate-list-create'),
    path('heart_rates/<int:pk>/', HeartRateDetailView.as_view(), name='heart-rate-detail'),
]
