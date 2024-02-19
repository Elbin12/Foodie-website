from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.core.validators import RegexValidator
import secrets
from adminpage.adminpage.models import *
from products.models import *
from django.db.models import Sum
from decimal import Decimal
from datetime import timedelta,datetime
from django.conf import settings
from os.path import basename

# Create your models here.


class Profile(BaseModel):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender=models.CharField(null=True)
    is_email_verified = models.BooleanField(default=False)
    block=models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    mobile_number= models.CharField(max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Mobile number must be 10 digits.',
            ),
        ],
        blank=True, null=True,
    )

    
    
def generate_email_verification_token(self):
    return secrets.token_urlsafe(24)

class Address(BaseModel):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    name=models.CharField(null=True, blank=True)
    mobile_number= models.CharField(max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Mobile number must be 10 digits.',
            ),
        ],
        blank=True, null=True,
    )
    address=models.TextField(null=True, blank=True)
    pincode=models.IntegerField(null=True, blank=True)
    locality=models.CharField(null=True, blank=True)
    city=models.CharField(null=True, blank=True)
    state=models.CharField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
   

class Cart(BaseModel):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    applied_coupon=models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='applied_coupon', null=True)
    total=models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        price=Cart_item.objects.filter(cart=self).aggregate(Sum('price'))['price__sum'] or 0
        self.total=price
        super(Cart, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username
    
class Cart_item(BaseModel):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    product_attribute=models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='cart_items', default=True)
    qty=models.IntegerField(default=1)
    price=models.IntegerField(null=True, blank=True)
    is_added=models.BooleanField(default=False)

    def save(self , *args, **kwargs):
        decimal_qty=Decimal(self.qty)
        decimal_product_price=Decimal(self.product_attribute.new_price)
        decimal_price=decimal_qty*decimal_product_price
        self.price=int(decimal_price)
        super(Cart_item, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product.product_name
    


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        PREPARING = 'Preparing', 'Preparing'
        CANCELLED = 'Cancelled', 'Cancelled'
        DELIVERED = 'Delivered', 'Delivered'
        CANCELLED_BY_ADMIN= 'Cancelled by admin', 'Cancelled by admin'
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name=models.CharField(max_length=50, null=True)
    mob=models.CharField(max_length=10, null=True)
    address=models.CharField(max_length=500)
    order_status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    coupon_discount=models.CharField(null=True)
    subtotal=models.IntegerField(null=True)
    total_amount = models.DecimalField(max_digits=30, decimal_places=2)
    cancel_request=models.BooleanField(default=False)
    payment_method=models.CharField(max_length=100, null=True)

class Ordered_item(BaseModel):
    order_id=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_items')
    ordered_product_name=models.CharField(max_length=100, null=True)
    qty=models.IntegerField(default=1) 
    unit_price=models.IntegerField(null=True)
    price = models.IntegerField()
    image=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_items', null=True)
    product_variants = models.JSONField(null=True)

    def save(self, *args, **kwargs):
        decimal_qty = Decimal(self.qty)
        decimal_product_price = Decimal(self.unit_price)
        decimal_price = decimal_qty * decimal_product_price
        self.price = int(decimal_price)
        super(Ordered_item, self).save(*args, **kwargs)


class Payment(BaseModel):
    class PaymentMethod(models.TextChoices):
        COD = 'COD', 'COD'
        PAYMENT = 'Payment', 'Payment'

    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment', null=True)
    payment_method=models.CharField(choices=PaymentMethod.choices, default=PaymentMethod.COD)
    is_paid=models.BooleanField(default=False)
    razorpay_order_id=models.CharField(max_length=100, null=True, blank=True)
    rarzorpay_payment_id=models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_signature=models.CharField(max_length=100, null=True, blank=True)
    amount=models.IntegerField(null=True)

class Wallet(BaseModel):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallet' )
    balance=models.IntegerField(default=0, null=True)

class Transaction(BaseModel):
    class Type(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'deposit'
        PURCHASED_PRODUCT = 'PURCHASED_PRODUCT', 'purchased product'

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.IntegerField()
    transaction_type = models.CharField(choices=Type.choices, null=True)


class Wishlist(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(ProductAttribute, related_name='wishlists', blank=True)