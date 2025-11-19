# middleware.py
import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('request_logging')

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get user information
        user = self._get_user_info(request)
        
        # Get client IP
        ip = self._get_client_ip(request)
        
        # Process request
        start_time = datetime.now()
        response = self.get_response(request)
        duration = (datetime.now() - start_time).total_seconds()
        
        # Log the request
        log_message = (
            f"{datetime.now()} - "
            f"User: {user} - "
            f"IP: {ip} - "
            f"Path: {request.path} - "
            f"Method: {request.method} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration:.2f}s"
        )
        logger.info(log_message)
        
        return response
    
    def _get_user_info(self, request):
        """Safely get user information"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            return request.user.username
        return "Anonymous"
    
    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip