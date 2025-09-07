from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .models import RequestLog, BlockedIP

class IPLoggingMiddleware:
    """
    Middleware to:
    1. Log every request's IP, timestamp, and path.
    2. Block requests from blacklisted IPs.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract client IP
        ip = self.get_client_ip(request)

        if ip:
            # Check if the IP is in the blacklist
            if BlockedIP.objects.filter(ip_address=ip).exists():
                return HttpResponseForbidden("Forbidden: Your IP is blacklisted.")

            # Log the request
            RequestLog.objects.create(
                ip_address=ip,
                timestamp=now(),
                path=request.path
            )

        # Continue to the next middleware or view
        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Extracts the client's IP address, supporting proxies.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

