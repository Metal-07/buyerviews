from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Marks some products as featured'

    def handle(self, *args, **options):
        products = Product.objects.filter(price__gt=50)[:6]
        for product in products:
            product.featured = True
            product.save()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully marked {len(products)} products as featured')) 