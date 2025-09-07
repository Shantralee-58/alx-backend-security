from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    """
    Flags IPs exceeding 100 requests/hour or accessing sensitive paths (/admin, /login)
    """
    one_hour_ago = now() - timedelta(hours=1)
    sensitive_paths = ['/admin', '/login']

    # 1. Flag IPs exceeding 100 requests in the last hour
    from django.db.models import Count

    ip_counts = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(request_count=Count('id'))
        .filter(request_count__gt=100)
    )

    for entry in ip_counts:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            reason=f"Exceeded 100 requests/hour"
        )

    # 2. Flag IPs accessing sensitive paths
    for path in sensitive_paths:
        suspicious_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago, path__startswith=path)
        for log in suspicious_logs:
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                reason=f"Accessed sensitive path: {log.path}"
            )

