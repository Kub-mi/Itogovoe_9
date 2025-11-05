"""Celery tasks for the core application."""

from celery import shared_task


@shared_task
def ping() -> str:
    """Return a simple response to confirm Celery worker availability."""
    return "pong"
