import csv
from django.core.management.base import BaseCommand
from softv.models import Product, Category

class Command(BaseCommand):
    help = 'Load products and categories from CSV files into the database'

    def handle(self, *args, **kwargs):
        self.import_products()

    def import_products(self):
        with open('data/game.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Category.objects.get(name='gaming')
                price_int = int(row['price'].replace("₹", "").replace(",", "").strip())
                
                product, created = Product.objects.get_or_create(
                    name=row['title'],
                    category=category,
                    defaults={
                        'price': int(price_int),
                        'desc': row['about_product'],
                        'image': row['main_image'],
                        'company_name': row['title'].split()[0],
                        'quantity': 100
                    }
                )
                
                if not created:
                    # Update the existing product with new information
                    product.price = price_int
                    product.desc = row['about_product']
                    product.image = row['main_image']
                    product.company_name = row['title'].split()[0]
                    product.quantity = 100
                    product.save()
                
                print(f"Product {'created' if created else 'updated'}: {product.name}")

        self.stdout.write(self.style.SUCCESS('Products imported successfully'))
