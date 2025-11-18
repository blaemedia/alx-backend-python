from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner.
        return obj.owner == request.user


class IsMessageOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a message to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the sender or receiver of the message
        return obj.sender == request.user or obj.receiver == request.user


class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is one of the participants in the conversation
        return request.user in obj.participants.all()


class IsUserProfileOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own profile.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanAccessUserMessages(permissions.BasePermission):
    """
    Custom permission to ensure users can only access their own messages.
    """
    def has_permission(self, request, view):
        # For list views, check if user is accessing their own messages
        if hasattr(view, 'get_queryset'):
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Users can only access messages where they are sender or receiver
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return obj.sender == request.user or obj.receiver == request.user
        
        # For conversation objects, check if user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        # For user profiles, only allow access to own profile
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False