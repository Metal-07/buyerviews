import os
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.utils.text import slugify
from .models import Category, Product

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1cUkMqUdiF-mRmC58XOx9kTKDmXDSFieiA4OU_imUw0g'
RANGE_NAME = 'Sheet1!A2:L'  # Extending range to include more columns
SERVICE_ACCOUNT_FILE = 'service-account.json'

def get_google_sheets_service():
    """Gets Google Sheets API service with service account authentication."""
    try:
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            raise FileNotFoundError(
                'service-account.json file not found. Please download it from Google Cloud Console.'
            )

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except Exception as e:
        logger.error(f'Failed to build service: {str(e)}')
        raise

def clean_rating(rating_str):
    """Converts rating string to decimal."""
    try:
        if not rating_str:
            return None
        return float(rating_str)
    except (ValueError, TypeError):
        logger.warning(f'Failed to parse rating: {rating_str}')
        return None

def clean_reviews(reviews_str):
    """Converts reviews string to integer."""
    try:
        if not reviews_str:
            return None
        # Remove commas and convert to integer
        cleaned = ''.join(c for c in str(reviews_str) if c.isdigit())
        return int(cleaned) if cleaned else None
    except (ValueError, TypeError):
        logger.warning(f'Failed to parse reviews: {reviews_str}')
        return None

def import_data_from_sheets():
    """Imports data from Google Sheets into the database."""
    try:
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        values = result.get('values', [])

        if not values:
            logger.warning('No data found in the Google Sheet.')
            return

        # Keep track of processed items for logging
        processed_categories = set()
        processed_products = 0
        errors = []

        for row in values:
            try:
                if len(row) < 2:  # Need at least category and name
                    continue

                category_name = row[0].strip()
                product_name = row[1].strip()
                
                # Skip empty rows
                if not category_name or not product_name:
                    continue

                # Get or create category
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={'slug': slugify(category_name)}
                )
                processed_categories.add(category_name)

                # Extract other fields with safe defaults
                description = row[3] if len(row) > 3 else ''
                price = 'Check Price on Amazon'  # Default price text
                rating = clean_rating(row[5] if len(row) > 5 else None)  # Rating in column 6
                reviews = clean_reviews(row[6] if len(row) > 6 else None)  # Reviews in column 7
                image_url = row[7] if len(row) > 7 else ''  # Image URL in column 8
                affiliate_link = row[8] if len(row) > 8 else ''  # Affiliate link in column 9
                pros = row[9] if len(row) > 9 else ''  # Pros in column 10
                cons = row[10] if len(row) > 10 else ''  # Cons in column 11

                # Create or update product
                product, created = Product.objects.update_or_create(
                    name=product_name,
                    category=category,
                    defaults={
                        'description': description,
                        'price': price,
                        'rating': rating,
                        'reviews': reviews,
                        'image_url': image_url,
                        'affiliate_link': affiliate_link,
                        'pros': pros,
                        'cons': cons
                    }
                )
                processed_products += 1

            except Exception as e:
                error_msg = f'Error processing row {product_name}: {str(e)}'
                logger.error(error_msg)
                errors.append(error_msg)

        # Log summary
        logger.info(f'Import completed. Processed {len(processed_categories)} categories and {processed_products} products.')
        if errors:
            logger.warning(f'Encountered {len(errors)} errors during import.')
            for error in errors:
                logger.warning(error)

        return {
            'categories': len(processed_categories),
            'products': processed_products,
            'errors': len(errors)
        }

    except HttpError as e:
        error_msg = f'Google Sheets API error: {str(e)}'
        logger.error(error_msg)
        raise Exception(error_msg)
    except Exception as e:
        error_msg = f'Unexpected error during import: {str(e)}'
        logger.error(error_msg)
        raise Exception(error_msg)