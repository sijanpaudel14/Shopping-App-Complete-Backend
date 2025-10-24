from store.models import Product


# Preload related objects for better performance
Product.objects.select_related('...')
Product.objects.prefetch_related('...')

# Load only what you need
Product.objects.only('id', 'title', 'unit_price')
Product.objects.defer('description', 'last_update')

# Use values() or values_list() for read-only operations
Product.objects.values('id', 'title', 'unit_price')
Product.objects.values_list('id', 'title')

# Count related objects efficiently
from django.db.models import Count
Product.objects.count('reviews')
len(Product.objects.all()) # Less efficient

# Bulk create objects
products_to_create = [
    Product(title='Product 1', unit_price=10.00),
    Product(title='Product 2', unit_price=20.00),
]
Product.objects.bulk_create(products_to_create)


