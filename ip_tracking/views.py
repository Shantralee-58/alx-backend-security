from django.http import JsonResponse
from ratelimit.decorators import ratelimit
from ratelimit.core import is_ratelimited
from django.contrib.auth.decorators import login_required

# Example sensitive view
def sensitive_view(request):
    """
    Rate-limited sensitive endpoint.
    - Anonymous: 5 requests/minute
    - Authenticated: 10 requests/minute
    """
    # Determine rate limit based on authentication
    limit = '10/m' if request.user.is_authenticated else '5/m'

    # Check if the request exceeds the limit
    if is_ratelimited(request, key='ip', rate=limit, method='POST', increment=True):
        return JsonResponse({"error": "Too many requests. Try again later."}, status=429)

    # Example logic for the view
    if request.method == "POST":
        return JsonResponse({"message": "Request accepted"})
    else:
        return JsonResponse({"message": "Send a POST request"})

# Optional: a public test view without rate limiting
def test_view(request):
    return JsonResponse({"message": "Hello! This endpoint is not rate-limited."})

