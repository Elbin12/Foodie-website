
from django.urls import path
from . import views


app_name='adminpage'


urlpatterns = [
    path('custom/', views.admin_login, name='custom_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('home/', views.home, name='home' ),
    path('users/',views.users, name='users'),
    path('block_user/<id>', views.block_user,name='block_user'),
    path('edit/<id>', views.user_details, name='edit_user'),
    path('banner/', views.banner, name='banner'),
    path('delete_banner/<uid>', views.delete_banner, name='delete_banner'),
    path('orders/', views.orders, name='orders'),
    path('order_details/<uid>', views.order_details, name='order_details'),
    path('approve_cancel_request/<uid>', views.approve_cancel_request, name='approve_cancel_request'),
    path('coupons/', views.coupons, name='coupons'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('edit_coupon/<uid>', views.edit_coupon, name='edit_coupon'),
    path('activate_coupon/<uid>', views.activate_coupon, name='activate_coupon'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('export_data_to_excel/', views.export_data_to_excel, name='export_data_to_excel'),
]