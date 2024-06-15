from django.db import models
from author.models import AuthorProfile
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='products_category')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='products')
    price = models.IntegerField()
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)
    is_stock_avaialable = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} Image"

ORDER_STATUS_CHOICES = [
    ('PLACED', 'PLACED'),
    ('SHIPPED', 'SHIPPED'),
    ('OUT_FOR_DELIVERY', 'OUT FOR DELIVERY'),
    ('DELIVERED', 'DELIVERED')
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.CharField(max_length=255)
    details = models.TextField()
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
