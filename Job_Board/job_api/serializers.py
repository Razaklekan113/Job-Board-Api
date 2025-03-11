from rest_framework import serializers
from .models import ApplicantProfile, EmployerProfile, User, Job
from django.contrib.auth.hashers import check_password

# Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'password', 'password2', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 before creating user
        return User.objects.create_user(**validated_data)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'is_active', 'role']

# Employer Profile Serializer
class EmployerProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="user.email")
    full_name = serializers.ReadOnlyField(source="user.full_name")
    phone_number = serializers.ReadOnlyField(source="user.phone_number")

    class Meta:
        model = EmployerProfile
        fields = ['id', 'email', 'full_name', 'phone_number', 'company_name', 'website', 'industry', 'company_size']

# Applicant Profile Serializer
class ApplicantProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="user.email")
    full_name = serializers.ReadOnlyField(source="user.full_name")
    phone_number = serializers.ReadOnlyField(source="user.phone_number")

    class Meta:
        model = ApplicantProfile
        fields = ['id', 'email', 'full_name', 'phone_number', 'resume', 'skills', 'experience']

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email").lower()
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({"error": "User does not exist"})

        if not check_password(password, user.password):
            raise serializers.ValidationError({"error": "Invalid credentials"})

        attrs["user"] = user
        return attrs

# Job Serializer
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
