from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignments, Notification  # Import your models

@receiver(post_save, sender=Assignments)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the engineer
        notification = Notification.objects.create(
            assignment=instance,  # Use the 'assignment' field
            engineer=instance.engineer,
            message='You have been assigned to the Item.',
            link=f'/assignment/{instance.id}',
        )
