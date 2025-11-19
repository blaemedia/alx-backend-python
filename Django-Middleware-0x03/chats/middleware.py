# chats/middleware.py
import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

# Get logger instance
logger = logging.getLogger('request_logging')

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get user information safely
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        
        # Process the request and get response
        response = self.get_response(request)
        
        # Log the request information
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path} - Method: {request.method} - Status: {response.status_code}"
        logger.info(log_message)
        
        return response