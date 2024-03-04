from django.db import models
from base.models import BaseModel
from django.core.validators import MinValueValidator
from datetime import timedelta
from django.utils import timezone
from datetime import datetime



# Create your models here.


class Coupon(BaseModel):
    coupon_code=models.CharField(max_length=100)
    is_expired=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=100)
    minimum_amount=models.IntegerField(default=400)
    no_of_coupons=models.IntegerField(default=10,validators=[MinValueValidator(0)])
    expire_date=models.DateTimeField(default=True)
    
    def save(self, *args, **kwargs):
        if int(self.no_of_coupons) == 0  :
            self.is_expired=True
        super(Coupon, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.coupon_code