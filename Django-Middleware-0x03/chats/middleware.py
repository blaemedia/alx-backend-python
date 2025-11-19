# middleware.py
import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.utils import timezone
from collections import defaultdict, deque

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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store IP addresses and their message timestamps
        self.message_timestamps = defaultdict(deque)
        self.limit = 5  # 5 messages per minute
        self.window_seconds = 60  # 1 minute window
    
    def __call__(self, request):
        # Get client IP address
        ip_address = self.get_client_ip(request)
        
        # Check if this is a POST request to chat/message endpoints
        is_chat_post = (request.method == 'POST' and 
                       any(path in request.path for path in ['/chats/', '/conversations/', '/messages/']))
        
        if is_chat_post:
            current_time = timezone.now()
            
            # Clean old timestamps (older than 1 minute)
            self.clean_old_timestamps(ip_address, current_time)
            
            # Check if user has exceeded the limit
            if len(self.message_timestamps[ip_address]) >= self.limit:
                user = request.user.username if request.user.is_authenticated else "Anonymous"
                error_message = f"Rate limit exceeded. Maximum {self.limit} messages per minute allowed. Please wait before sending more messages."
                print(f"BLOCKED: {datetime.now()} - User: {user} - IP: {ip_address} - Path: {request.path} - Reason: Rate limit exceeded")
                return HttpResponseForbidden(error_message)
            
            # Add current timestamp for this IP
            self.message_timestamps[ip_address].append(current_time)
            
            # Log the message count for monitoring
            user = request.user.username if request.user.is_authenticated else "Anonymous"
            print(f"MESSAGE: {datetime.now()} - User: {user} - IP: {ip_address} - Messages in last minute: {len(self.message_timestamps[ip_address])}")
        
        # Process the request
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def clean_old_timestamps(self, ip_address, current_time):
        """Remove timestamps older than 1 minute"""
        if ip_address in self.message_timestamps:
            # Remove timestamps older than the time window
            while (self.message_timestamps[ip_address] and 
                   (current_time - self.message_timestamps[ip_address][0]).total_seconds() > self.window_seconds):
                self.message_timestamps[ip_address].popleft()


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        return response