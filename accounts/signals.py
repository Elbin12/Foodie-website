from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Cart, Cart_item

@receiver(post_save, sender=Product)
def update_cart_total_if_product_listed(sender, instance, **kwargs):
    cart_items = Cart_item.objects.filter(product=instance)
    updated_carts = set()

    for item in cart_items:
        cart = item.cart
        cart.total = sum(
            i.price for i in cart.cart_items.all()
        )
        cart.save()
        updated_carts.add(cart.uid)

    print(f"Updated carts: {updated_carts}")
