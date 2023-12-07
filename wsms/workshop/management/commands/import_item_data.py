import csv
from django.core.management.base import BaseCommand
from workshop.models import Item
class Command(BaseCommand):
    help = 'Import Item data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        self.load_stock_data_from_csv(file_path)

    def load_stock_data_from_csv(self, file_path):
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Item.objects.create(
                    number=row['number'],
                    description=row['description'],
                    
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported stock data'))


