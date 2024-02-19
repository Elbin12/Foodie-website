
from django.urls import path
from . import views

app_name='product'


urlpatterns = [
    path('all-products/', views.products, name='products' ),
    path('add-product/', views.add_product, name='add_product' ),
    path('edit/<uid>', views.edit_product, name='edit_product' ),
    path('edit_image/', views.edit_image, name='edit_image'),
    path('delete_image/', views.delete_image, name='delete_image'),
    path('delete/<uid>', views.delete_product, name='delete_product'),
    path('get_sub_categories/', views.get_sub_categories, name='get_sub_categories'),
    path('add_product_attributes/', views.add_product_attributes, name='add_product_attributes'),
    path('get_attribute_values/', views.get_attribute_values, name='get_attribute_values'),
    path('get_attributes/', views.get_attributes, name='get_attributes'),
    path('product_attributes/', views.product_attributes, name='product_attributes'),
    path('edit_product_attribute/<uid>', views.edit_product_attribute, name='edit_product_attribute'),
    
]
