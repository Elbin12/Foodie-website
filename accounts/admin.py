from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Cart_item)

admin.site.register(Address)

admin.site.register(Order)

admin.site.register(Ordered_item)

admin.site.register(Payment)

admin.site.register(Wallet)

admin.site.register(Transaction)

admin.site.register(Wishlist)