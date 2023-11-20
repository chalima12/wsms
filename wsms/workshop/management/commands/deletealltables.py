from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Delete all tables in the database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = [row[0] for row in cursor.fetchall()]

            for table in tables:
                cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')

        self.stdout.write(self.style.SUCCESS('All tables deleted successfully.'))
