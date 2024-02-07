
from django.urls import path
from . import views


app_name='category'


urlpatterns = [
    path('add-category/', views.add_category, name='add_category'),
    path('edit_category/<uid>', views.edit_category, name='edit_category'),
    path('delete_category/<uid>', views.delete_category, name='delete_category'),
    path('subcategory/<uid>', views.add_sub_category, name='add_sub_category'),
    path('edit-subcategory/<uid>', views.edit_subcategory, name='edit_subcategory'),
    path('delete-subcategory/<uid>', views.delete_sub_category, name='delete_sub_category')
]