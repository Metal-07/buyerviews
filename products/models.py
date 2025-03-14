from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_product_count(self):
        return self.products.count()

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    price = models.CharField(max_length=50, default='Check Price on Amazon')  # Changed to CharField
    image_url = models.URLField(max_length=1000, blank=True)
    affiliate_link = models.URLField(max_length=1000, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    reviews = models.IntegerField(null=True, blank=True)
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def short_description(self):
        words = self.description.split()
        if len(words) > 20:
            return ' '.join(words[:20]) + '...'
        return self.description
