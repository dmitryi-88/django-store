import logging
import time
from typing import Any

logger = logging.getLogger("django.request")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()

        response = self.get_response(request)
        duration = time.perf_counter() - start_time
        ip_address = self.get_client_ip(request)

        logger.info(
            "IP: %s | URL: %s | Method: %s | " "Status: %s | Duration: %.4f sec",
            ip_address,
            request.get_full_path(),
            request.method,
            response.status_code,
            duration,
        )

        return response

    @staticmethod
    def get_client_ip(request):
        return request.META.get("REMOTE_ADDR", "Unknown")
