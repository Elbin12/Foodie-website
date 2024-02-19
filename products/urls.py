
from django.urls import path
from . import views


app_name='products'

urlpatterns = [
    path('product/<uid>', views.get_product, name='product'),
    path('get_value_price/', views.get_value_price, name='get_value_price'),
    path('selectvariants/', views.selectvariants, name='selectvariants'),
    path('shop_page/', views.shop_page, name='shop_page'),
    path('categories/<uid>', views.categories, name='categories'),
    path('checkout/<uid>', views.checkout, name='checkout'),
    path('checkout/', views.checkout, name='cart_checkout'),
    path('paymenthandler/<amount>', views.paymenthandler, name='paymenthandler'),
    path('order_success/<uid>', views.order_success, name='order_success'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
]