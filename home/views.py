from django.shortcuts import render
from products.models import Product,Category
from accounts.models import Cart, Cart_item
from home.models import Banner
from django.contrib.auth.models import User

# Create your views here.



def home(request):
    products=Product.objects.filter(is_listed=True ,is_category_listed=True).order_by('product_name')
    # cart=Cart.objects.get(user=request.user)
    # cart_items=Cart_item.objects.get(cart=cart)
    # print(cart_items)
    # print(item.is_added)
    # for i in cart_items:
    #     if i.is_added==True:
    #         print('added')
    context={
        'products':products,
        'categories':Category.objects.filter(is_listed=True).order_by('category_name'),
        # 'cart':cart
        'banners':Banner.objects.all().order_by('order'),
        'is_authenticated':request.user.is_authenticated
        }
    banners=Banner.objects.all()
    for banner in banners:
        print(banner)

    return render(request, 'home/home.html',context)


