from django.core.management.base import BaseCommand
from products.utils import import_data_from_sheets
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import data from Google Sheets'

    def handle(self, *args, **options):
        self.stdout.write('Starting data import from Google Sheets...')
        try:
            result = import_data_from_sheets()
            self.stdout.write(self.style.SUCCESS(
                f'Successfully imported {result["products"]} products in {result["categories"]} categories.'
            ))
            if result["errors"] > 0:
                self.stdout.write(self.style.WARNING(
                    f'Encountered {result["errors"]} errors during import. Check the logs for details.'
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to import data: {str(e)}'))
            logger.error(f'Import failed: {str(e)}') 