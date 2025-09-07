from .models import RequestLog
from django.utils.timezone import now

class IPLoggingMiddleware:
    """
    Middleware to log IP address, timestamp, and path for every request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract the client's IP
        ip = self.get_client_ip(request)

        # Save request log to the database
        if ip:
            RequestLog.objects.create(
                ip_address=ip,
                timestamp=now(),
                path=request.path
            )

        # Continue processing the request
        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Extracts client IP address even if behind a proxy.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

