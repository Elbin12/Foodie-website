
from django.urls import path
from . import views

app_name='account'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.app_logout, name='app_logout'),
    path('otp_verification/',views.otp_verification,name="otp_verification"),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify/', views.verify, name='verify'),
    path('resend/', views.resend, name='resend'),
    path('', views.account, name='account'),
    path('addresses/', views.manage_addresses, name='addresses'),
    path('edit_address/<uid>/', views.edit_address, name='edit_address'),
    path('edit_address_from_checkout/', views.edit_address_from_checkout, name='edit_address_from_checkout'),
    path('add_address_from_checkout/', views.add_address_from_checkout, name='add_address_from_checkout'),
    path('delete_address/',views.delete_address, name='delete_address'),
    path('add_to_cart/',views.add_to_cart,name="add_to_cart"),
    path('cart/',views.cart, name='cart'),
    path('change/',views.change, name='change'),
    path('delete/',views.delete, name='delete'),
    path('my_orders/' ,views.my_orders, name='my_orders'),
    path('order/<uid>' ,views.order_details, name='order_details'),
    path('cancel_request/<uid>' ,views.cancel_request, name='cancel_request'),
    path('coupons/' ,views.coupons, name='coupons'),
    path('wallet/' ,views.wallet, name='wallet'),
    path('paymenthandler/<amount>' ,views.paymenthandler, name='paymenthandler'),
    path('check_otp/', views.check_otp, name='check_otp'),
]