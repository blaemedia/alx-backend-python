# middleware.py
import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden

# Create a logger
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get user information
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        
        # Log the request information
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        # Print to console for immediate feedback
        print(log_message)
        
        # Process the request
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get current time
        current_time = datetime.now().time()
        
        # Define restricted hours (9 PM to 6 AM) - outside these hours access is denied
        start_restriction = time(21, 0)  # 9:00 PM
        end_restriction = time(6, 0)     # 6:00 AM
        
        # Check if current time is within restricted hours
        is_restricted = False
        if start_restriction <= end_restriction:
            # Normal case: restriction within same day
            is_restricted = start_restriction <= current_time <= end_restriction
        else:
            # Overnight case: restriction spans midnight
            is_restricted = current_time >= start_restriction or current_time <= end_restriction
        
        # Check if the request is for chat-related paths
        is_chat_path = any(path in request.path for path in ['/chats/', '/conversations/', '/messages/'])
        
        # Deny access if it's restricted time and chat path
        if is_restricted and is_chat_path:
            user = request.user.username if request.user.is_authenticated else "Anonymous"
            error_message = f"Access denied. Chat service is only available between 6:00 AM and 9:00 PM. Current time: {current_time.strftime('%H:%M')}"
            print(f"BLOCKED: {datetime.now()} - User: {user} - Path: {request.path} - Reason: Outside allowed hours")
            return HttpResponseForbidden(error_message)
        
        # If not restricted, process the request normally
        response = self.get_response(request)
        return response