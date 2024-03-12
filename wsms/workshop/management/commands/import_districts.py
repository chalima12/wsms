import pandas as pd
from django.core.management.base import BaseCommand
from workshop.models import District

class Command(BaseCommand):
    help = 'Import districts from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            # Iterate over each row and create District objects
            for index, row in df.iterrows():
                name = row['name']
                region = row['region']
                # Create District object
                district = District.objects.create(name=name, region=region)
                self.stdout.write(self.style.SUCCESS(f'District created: {district}'))
            self.stdout.write(self.style.SUCCESS('Districts imported successfully'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
