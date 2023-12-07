from django.core.management.base import BaseCommand
from workshop.models import Item  # Import your Item model

class Command(BaseCommand):
    help = 'Delete items with specified criteria'

    def add_arguments(self, parser):
        # Add arguments for delete criteria
        parser.add_argument('--status', type=str, help='Delete items with the specified status')
        parser.add_argument('--section', type=str, help='Delete items in the specified section')
        parser.add_argument('--is_valid', action='store_true', help='Delete valid items')
        parser.add_argument('--engineer', type=str, help='Delete items assigned to the specified engineer')

    def handle(self, *args, **options):
        # Construct the filter criteria based on command-line arguments
        filter_criteria = {}

        if options['status']:
            filter_criteria['status'] = options['status']

        if options['section']:
            filter_criteria['Section__name'] = options['section']

        if options['is_valid']:
            filter_criteria['is_valid'] = False

        if options['engineer']:
            filter_criteria['engineer__username'] = options['engineer']

        # Fetch items based on filter criteria
        items_to_delete = Item.objects.filter(**filter_criteria)

        # Display a summary of items to be deleted
        self.stdout.write(self.style.SUCCESS(f'{items_to_delete.count()} items found for deletion.'))

        # Ask for confirmation before proceeding with deletion
        user_confirmation = input('Do you want to proceed with deletion? (yes/no): ')
        if user_confirmation.lower() == 'yes':
            # Perform the deletion
            items_to_delete.delete()
            self.stdout.write(self.style.SUCCESS('Items deleted successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('Deletion aborted.'))
