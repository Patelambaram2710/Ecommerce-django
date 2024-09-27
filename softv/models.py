from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    company_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    image = models.URLField()  # Change this to URLField if it's an online image URL
    desc = models.CharField(max_length=3000)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Using Decimal for currency precision


    def __str__(self):
        return f'{self.name} ({self.category.name})'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} ({self.product.category.name})'
    
    def get_total_price(self):
        """ Calculate the total price of this order """
        return self.price * self.quantity

class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateField(default=timezone.now)  # Replace with timezone.now

    
class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    cart_item_ids = models.CharField(max_length=255, default=None, blank=True)  # Consider using ManyToManyField with Cart
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Using Decimal for currency precision
    address = models.CharField(max_length=500, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    date = models.DateField(default=timezone.now)  # Replace with timezone.now
    payment = models.BooleanField(default=False)
    status = models.BooleanField(default=False)



    def __str__(self):
        return f'Order #{self.id} by {self.customer.username}'

    def placeOrder(self,cart_id):
        self.save()

    @staticmethod
    def get_orders_by_customer(user_id):
        return Order.objects.filter(User=user_id).order_by('-date')

   
class Review(models.Model):
    text = models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username