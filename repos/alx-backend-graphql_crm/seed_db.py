
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from crm.models import Customer, Product

def seed_data():
    # Create Customers
    Customer.objects.create(name="Alice", email="alice@example.com", phone="+1234567890")
    Customer.objects.create(name="Bob", email="bob@example.com", phone="123-456-7890")
    Customer.objects.create(name="Charlie", email="charlie@example.com")

    # Create Products
    Product.objects.create(name="Laptop", price=999.99, stock=10)
    Product.objects.create(name="Mouse", price=25.00, stock=50)
    Product.objects.create(name="Keyboard", price=75.50, stock=30)

    print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
