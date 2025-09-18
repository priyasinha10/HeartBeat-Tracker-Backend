from rest_framework import serializers
from .models import User, Patient, HeartRate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import HeartRate

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'is_doctor']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'doctor']
        read_only_fields = ['doctor'] 


class HeartRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeartRate
        fields = ['id', 'patient', 'rate', 'recorded_at']
        read_only_fields = ['recorded_at']

