from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class product(models.Model):
    name=models.CharField(max_length=100,null=True)
    price=models.IntegerField(null=True)
    stock=models.IntegerField(null=True)
    product_image=models.ImageField(upload_to='media/',null=True)
    categ=models.ForeignKey('category', on_delete=models.CASCADE, null=True, related_name='products')
    description = models.TextField(null=True)
    def __str__(self):
        return self.name

class User_details(models.Model):
    Name=models.CharField(max_length=30,null=True)
    email=models.EmailField(max_length=50,null=True)
    Mobile_No=models.CharField(null=True)
    password=models.CharField(max_length=40,null=True)
    def __str__(self):
        return self.Name


class category(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class employee(models.Model):
    name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name
    
class task(models.Model):
    taskName = models.CharField(max_length=100, null=True)
    emp=models.OneToOneField(employee, on_delete=models.CASCADE, null=True, related_name='tasks')
    def __str__(self):
        return self.taskName
    
class book(models.Model):
    bookName = models.CharField(max_length=100, null=True)
    pub=models.ManyToManyField(employee, related_name='books', null=True)
    def __str__(self):
        return self.bookName

class publisher(models.Model):
    pubname = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.pubname
    
class admin_order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class admin_order_item(models.Model):
    order = models.ForeignKey(admin_order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order
    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Order #{self.order.id})"