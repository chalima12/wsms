from django.core.management.base import BaseCommand
from workshop.models import *  # Replace 'yourapp' with the name of your Django app

class Command(BaseCommand):
    help = 'Delete all rows from the Stock model'

    def handle(self, *args, **options):
        Component.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all rows from Stock model'))
