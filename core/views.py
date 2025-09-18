from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Patient,HeartRate
from .serializers import UserRegisterSerializer, PatientSerializer,HeartRateSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_doctor'] = user.is_doctor
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            is_many = isinstance(data, list)

            serializer = self.get_serializer(data=data, many=is_many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HeartRateListCreateView(generics.ListCreateAPIView):
    queryset = HeartRate.objects.all()
    serializer_class = HeartRateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            is_many = isinstance(data, list)
            
            serializer = self.get_serializer(data=data, many=is_many)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Something went wrong", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HeartRateDetailView(generics.RetrieveAPIView):
    queryset = HeartRate.objects.all()
    serializer_class = HeartRateSerializer
    permission_classes = [permissions.IsAuthenticated]


