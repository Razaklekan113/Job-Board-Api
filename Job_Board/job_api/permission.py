from rest_framework.permissions import BasePermission

class IsEmployer(BasePermission):
    """Allow access only to Employers"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employer'

class IsApplicant(BasePermission):
    """Allow access only to Applicants"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'applicant'

