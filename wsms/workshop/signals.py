from django.dispatch import receiver
from django.urls import reverse
from django.dispatch import Signal
from workshop.models import Notification
from workshop import signals


class ItemAssignedSignal(signals.Signal):
    def notify_engineer_item_assigned(sender, **kwargs):
        # Get the Item and engineer that were assigned.
        item = kwargs['item']
        engineer = kwargs['engineer']

    # Create a notification for the engineer.
        notification = Notification.objects.create(
            user=engineer,
            message=f'You have been assigned to the Item {item.Serial_no}.',
            link=reverse('assignments:detail', args=[item.id])
        )

    # Send the notification to the engineer.
        notification.send()


# @receiver(ItemAssignedSignal)
# def notify_engineer_item_assigned(sender, **kwargs):
#     # Get the Item and engineer that were assigned.
#     item = kwargs['item']
#     engineer = kwargs['engineer']

#     # Create a notification for the engineer.
#     notification = Notification.objects.create(
#         user=engineer,
#         message=f'You have been assigned to the Item {item.name}.',
#         link=reverse('assignments:detail', args=[item.id])
#     )

#     # Send the notification to the engineer.
#     notification.send()
