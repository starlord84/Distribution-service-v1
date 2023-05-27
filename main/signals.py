from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Distribution
from .tasks import send_request_to_url


@receiver(post_save, sender=Distribution)
def schedule_request(sender, instance, created, **kwargs):
    if created and instance.start_date > timezone.now():
        delay = (instance.start_date - timezone.now()).total_seconds()
        send_request_to_url.apply_async(args=[instance.id], countdown=delay)
