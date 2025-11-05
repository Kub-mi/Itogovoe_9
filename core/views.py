"""API views for the project."""

import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import ping

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """Simple API view to verify the service is running."""

    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request, *args, **kwargs):  # noqa: D401
        """Return application health status."""
        # Trigger asynchronous task to validate Celery configuration.
        try:
            ping.delay()
        except Exception:  # pragma: no cover - Celery might be offline locally.
            logger.warning("Celery is unavailable to execute ping task", exc_info=True)
        return Response({"status": "ok"})
