import pandas as pd
from django.core.management.base import BaseCommand
from workshop.models import Stock  

class Command(BaseCommand):
    help = 'Import stock data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        self.load_stock_data_from_excel(file_path)

    def load_stock_data_from_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)  # Read Excel file into DataFrame
            for index, row in df.iterrows():
                Stock.objects.create(
                    number=row['number'],
                    description=row['description'],
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported stock data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred while importing stock data: {str(e)}'))
