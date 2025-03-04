from rest_framework import serializers
from .models import User, UserProfile, Job
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

# Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)  # Ensure role selection

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
        user = User.objects.create_user(**validated_data)
        return user
    
# User Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'is_active', 'role']

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="user.email")
    full_name = serializers.CharField(source="user.full_name", required=False)
    phone_number = serializers.CharField(source="user.phone_number", required=False)
    role = serializers.CharField(source="user.role", required=False)  

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'full_name', 'phone_number', 'role']

    def update(self, instance, validated_data):
        user = instance.user  # Get related User model

        # Update user fields correctly
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            user.full_name = user_data.get('full_name', user.full_name)
            user.phone_number = user_data.get('phone_number', user.phone_number)
            user.role = user_data.get('role', user.role)
            user.save()

        return instance

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email").lower()
        password = attrs.get("password")

        # Check if user exists
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({"error": "User does not exist"})

        # Authenticate manually (Django expects 'username' but we use 'email')
        if not check_password(password, user.password):
            raise serializers.ValidationError({"error": "Invalid credentials"})

        attrs["user"] = user
        return attrs


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"