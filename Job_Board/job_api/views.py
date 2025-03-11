from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, ApplicantProfile, EmployerProfile
from .serializers import (
    RegisterSerializer, LoginSerializer, EmployerProfileSerializer,
    ApplicantProfileSerializer, JobSerializer
)
from .renderers import UserRenderer

# Token generation function
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# User Registration View
class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg": "Registration Successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Employer Profile View
class EmployerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'employer':
            return Response({"error": "Only employers can access this profile."}, status=status.HTTP_403_FORBIDDEN)

        profile, _ = EmployerProfile.objects.get_or_create(user=request.user)
        serializer = EmployerProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        if request.user.role != 'employer':
            return Response({"error": "Only employers can update this profile."}, status=status.HTTP_403_FORBIDDEN)

        profile = request.user.employer_profile
        serializer = EmployerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Applicant Profile View
class ApplicantProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'applicant':
            return Response({"error": "Only applicants can access this profile."}, status=status.HTTP_403_FORBIDDEN)

        profile, _ = ApplicantProfile.objects.get_or_create(user=request.user)
        serializer = ApplicantProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        if request.user.role != 'applicant':
            return Response({"error": "Only applicants can update this profile."}, status=status.HTTP_403_FORBIDDEN)

        profile = request.user.applicant_profile
        serializer = ApplicantProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token = get_tokens_for_user(user)

            return Response(
                {"token": token, "msg": "Login Successful"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Logout View
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
