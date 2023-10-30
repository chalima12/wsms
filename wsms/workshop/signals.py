from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from .models import Item, Notification

@receiver(post_save, sender=Item)
def create_notification(sender, instance, created, **kwargs):
    # If the item is newly created, assign it to a random engineer and create a notification
    if created:
        engineer = User.objects.filter(user_type='Engineer').order_by('?').first()
        instance.assigned_to = engineer
        instance.save()
        notification = Notification.objects.create(item=instance, engineer=engineer, status='pending')
    # If the item is updated and assigned to a different engineer, create a notification for the new engineer
    else:
        notification = Notification.objects.filter(item=instance).first()
        if notification and notification.engineer != instance.assigned_to:
            notification.engineer = instance.assigned_to
            notification.status = 'pending'
            notification.save()