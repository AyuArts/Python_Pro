from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Ad

@receiver(post_save, sender=Ad)
def deactivate_ad_after_30_days(sender, instance, **kwargs):
    if (timezone.now() - instance.created_at).days >= 30 and instance.is_active:
        instance.is_active = False
        instance.save()
