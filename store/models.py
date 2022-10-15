from django.db import models
from authentication.models import CustomUser


class Product(models.Model):
    name = models.CharField(max_length=44)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField()

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.customer.fio} {self.transaction_id}'
    
    @property
    def get_total_order_price(self):
        order_items = self.orderitem_set.all()
        total_price = sum(item.get_total_items_price for item in order_items)
        return total_price
    
    @property
    def get_total_order_quantity(self):
        order_items = self.orderitem_set.all()
        total_quantity = sum(item.quantity for item in order_items)
        return total_quantity


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.SmallIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.order.customer.fio} - {self.product}'
    
    @property
    def get_total_items_price(self):
        total_price = self.product.price * self.quantity
        return total_price
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name="shippingaddress")
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.customer.fio} {self.order.transaction_id}'