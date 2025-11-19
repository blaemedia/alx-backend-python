# chats/permissions.py
from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    """
    Only allow owners to perform any action (including PUT, PATCH, DELETE)
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check various common owner field names
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        if hasattr(obj, 'author'):
            return obj.author == request.user
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        # Default: only allow if user matches the object (for User model)
        return obj == request.user


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in SAFE_METHODS:
            return True

        # Write permissions (PUT, PATCH, DELETE) are only allowed to the owner
        return IsOwner().has_object_permission(request, view, obj)


class IsMessageParticipant(BasePermission):
    """
    Custom permission to only allow participants of a message to access it.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS for participants
        if request.method in SAFE_METHODS:
            if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
                return request.user in [obj.sender, obj.receiver]
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            return False
        
        # Allow PUT, PATCH, DELETE only for specific conditions
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # Use IsOwner permission for write operations
            return IsOwner().has_object_permission(request, view, obj)
        
        return False


class AllowAllForParticipants(BasePermission):
    """
    Allow all methods (GET, POST, PUT, PATCH, DELETE) for participants
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if user is a participant
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return request.user in [obj.sender, obj.receiver]
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class IsAuthenticated(BasePermission):
    """
    Simple permission that only checks if user is authenticated
    This is similar to DRF's IsAuthenticated but included for completeness
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For simple authentication, allow access to any object if user is authenticated
        return request.user and request.user.is_authenticated
    

class IsSenderOrReceiver(permissions.BasePermission):
    """
    Object-level permission to only allow sender or receiver of a message to view/edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read/write permissions are only allowed to the sender or receiver of the message
        return obj.sender == request.user or obj.receiver == request.user

