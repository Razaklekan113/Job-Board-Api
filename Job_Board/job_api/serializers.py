from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth import authenticate

# Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 before creating the user
        user = User.objects.create_user(**validated_data)
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"error": "Invalid credentials"})
        return attrs

# User Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'is_active']

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name")
    phone_number = serializers.CharField(source="user.phone_number")

    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'phone_number']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Update user fields
        if 'full_name' in user_data:
            instance.user.full_name = user_data['full_name']
        if 'phone_number' in user_data:
            instance.user.phone_number = user_data['phone_number']
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  # Ensure UserProfile is saved
        return instance
