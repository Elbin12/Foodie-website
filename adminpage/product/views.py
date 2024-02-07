from django.shortcuts import render, redirect
from products.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
import json

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def products(request):
    products=Product.objects.all().order_by('product_name')
    context={
        'products':products,
    }
    return render(request, 'adminpage/products/products.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def add_product(request):
    categories=Category.objects.all()
    sub_categories=Sub_category.objects.all()
    attributes=Attributes.objects.all()
    for i in attributes:
        attribute_values = i.attribute_values.all()
        # values.extend(attribute_value.value for attribute_value in attribute_values)
    context={'categories':categories, 'sub_categories':sub_categories,'values':attribute_values, 'attributes':attributes}
    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        images=request.FILES.getlist('image')
        price=request.POST.get('price')
        category=request.POST.get('category')
        sub_category=request.POST.get('sub_category')
        # values=request.POST.getlist('selected')
        # print(values)
        # attribute_values = Attribute_values.objects.filter(value__in=values)
        # print(attribute_values)


        selected_values = {}
        for i in attributes:
            checkbox_name = f'selected_{i.name}'
            if checkbox_name in request.POST:
                values=request.POST.getlist(checkbox_name)
                selected_values[i.name] = values

        print(selected_values)
                

        category_instance=Category.objects.get(category_name=category)
        sub_category_instance=Sub_category.objects.get(sub_category_name=sub_category)


        if Product.objects.filter(product_name=title).exists():
            messages.warning(request,'product is already exists')
            return redirect('product:add_product')


        product=Product.objects.create(product_name=title, Category=category_instance, Sub_category=sub_category_instance, price=price, product_description=description)

        for image in images:
            ProductImage.objects.create(product=product,image=image)

        # for values in selected_values.items():
        #     product_attribute=ProductAttribute.objects.create(product=product)
            
        for key, values in selected_values.items():
            for value in values:
                product_attribute = ProductAttribute.objects.create(product=product)
                print(value, 'agarsah')

                attribute = Attributes.objects.get(name=key)
                v = Attribute_values.objects.get(attribute=attribute, value=value)
                product_attribute.value.add(v)

                if value == 'Full':
                    print('full')
                    product_attribute.new_price = product.price
                elif value == 'quarter':
                    print('quarter')
                    product_attribute.new_price = int(product.price) / 4
                else:
                    print('half')
                    product_attribute.new_price = int(product.price) / 2

                print(product_attribute.new_price)

                product_attribute.save()

        
        # product_attribute=ProductAttribute.objects.create(product=product)
        # product_attribute.value.set(attribute_values)
        # product_attribute.save()


    return render(request, 'adminpage/products/add_product.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def edit_product(request,uid):
    product=Product.objects.get(uid=uid)
    categories=Category.objects.exclude(category_name=product.Category)
    sub_categories=Sub_category.objects.exclude(sub_category_name=product.Sub_category)

    images=ProductImage.objects.filter(product=product)
    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        images=request.FILES.getlist('image')
        price=request.POST.get('price')
        category=request.POST.get('category')
        sub_category=request.POST.get('sub_category')

        category_instance=Category.objects.get(category_name=category)
        sub_category_instance=Sub_category.objects.get(sub_category_name=sub_category)
        

        product.product_name=title
        product.product_description=description
        product.price=price
        product.Category=category_instance
        product.Sub_category=sub_category_instance
        

        for image in images:
            ProductImage.objects.create(product=product, image=image)
        product.save()

        images=product.product_images.all()
        
    context={'product':product, 'categories':categories, 'sub_categories':sub_categories,'images':images}
    return render(request, 'adminpage/products/edit_product.html',context)

def edit_image(request):
    if request.method=='POST':
        new_image_file = request.FILES.get('new_image')
        uid=request.POST.get('uid')
        print(uid,new_image_file)


        product_image = get_object_or_404(ProductImage, uid=uid)

        # checking_image=ProductImage.objects.filter(image=new_image_file)

        # if checking_image.exists():
        #     data = {'error': 'image is already exists'}
        #     return JsonResponse(data)            

        if new_image_file:
            product_image.image = new_image_file
            product_image.save()
            image=product_image.image.url
            image_name=product_image.image.name
            data={'data':uid, 'image':image, 'image_name':image_name}
        else:
            data = {'error': 'No new image provided'}
        return JsonResponse(data)
    

def delete_image(request):
    if request.method=='POST':
        uid=json.loads(request.body)['uid']
        print(uid)
        image=ProductImage.objects.get(uid=uid)
        image.delete()
        data={'success':'Image deleted successfully'}
        return JsonResponse(data)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def delete_product(request,uid):
    product=Product.objects.get(uid=uid)
    product.is_listed=not product.is_listed
    product.save()
    return redirect('product:products')

def get_sub_categories(request):
    if request.method=='POST':
        cat=json.load(request)['category']
        if cat=='':
            data={'sub_categories':''}
        else:
            c=Category.objects.get(category_name=cat)
            sub_categories=c.sub_categories.all()
            sub_categories_list = list(sub_categories.values())
            data={'sub_categories':sub_categories_list}
    else:
        data={'sub_categories':'Invalid HTTP method'}
        return JsonResponse(data)
    return JsonResponse(data)


