from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication with additional validation
    """
    def authenticate(self, request):
        header = self.get_header(request)
        
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        
        # Additional custom validation
        user = self.get_user(validated_token)
        
        # Check if user is active
        if not user.is_active:
            raise AuthenticationFailed('User is inactive')
            
        return (user, validated_token)


class IsTokenOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to access it
    """
    def has_object_permission(self, request, view, obj):
        # Assuming obj has a 'user' attribute
        return obj.user == request.user


class JWTAuth:
    """
    Base JWT authentication configuration for views
    """
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]


class JWTAuthWithOwnerPermission:
    """
    JWT authentication with owner permission check
    """
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsTokenOwner]