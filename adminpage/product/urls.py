
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
    path('get_sub_categories/', views.get_sub_categories, name='get_sub_categories')
]
