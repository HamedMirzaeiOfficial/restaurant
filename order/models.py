from account.models import User
from django.db import models
from coupon.models import Coupon
from restaurant.models import Food
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal



class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='order_user')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    postal_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.PositiveIntegerField()
    additional_information = models.TextField(blank=True, null=True)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, related_name='order', null=True,
                               blank=True, on_delete=models.SET_NULL)

    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), 
                                    MaxValueValidator(100)])
                                    
    class Meta: 
        ordering = ('-created',)
    
    def __str__(self):
        return f'Order {self.created}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / float((100))) * self.get_total_cost()
        return 0


    def get_total_cost_after_discount(self):
        return self.get_total_cost() - self.get_discount()

    def get_billing_status(self):
        if self.billing_status:
            return 'paid'
        else:
            return 'pending'
        


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Food, related_name='order_items', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity