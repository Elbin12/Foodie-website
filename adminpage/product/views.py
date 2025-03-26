from django.shortcuts import render, redirect
from products.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from adminpage.adminpage.views import is_superuser
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def products(request):
    products=Product.objects.all().order_by('product_name')
    categories = Category.objects.all()

    context={
        'categories':categories,
    }

    if request.method == 'GET':
        category = request.GET.get('category')
        date = request.GET.get('date')
        status = request.GET.get('status')
        if category and category != 'All category':
            products = products.filter(Category__category_name = category)
            context['selected_category'] = category
        if date:
            date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
            date_datetime = datetime.strptime(str(date), '%Y-%m-%d')
            products = products.filter(created_at__date=date_datetime)
            context['date'] = date
        if status == 'Active':
            products = products.filter(is_listed = True)
            context['status'] = status
        if status == 'Disabled':
            products = products.filter(is_listed = False)
            context['status'] = status

    context['products'] = products
    return render(request, 'adminpage/products/products.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def add_product(request):
    categories=Category.objects.all()
    sub_categories=Sub_category.objects.all()
    attributes=Attributes.objects.all()
    for i in attributes:
        attribute_values = i.attribute_values.all()
        # values.extend(attribute_value.value for attribute_value in attribute_values)
    context={'categories':categories, 'sub_categories':sub_categories, 'attributes':attributes}
    if request.method=='POST':
        print(request.POST, 'request data')
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


        # selected_values = {}
        # for i in attributes:
        #     checkbox_name = f'selected_{i.name}'
        #     if checkbox_name in request.POST:
        #         values=request.POST.getlist(checkbox_name)
        #         selected_values[i.name] = values

        # print(selected_values)
                

        category_instance=Category.objects.get(category_name=category)
        print('workinggggg.....',sub_category, Sub_category.objects.filter(sub_category_name=sub_category))
        sub_category_instance=Sub_category.objects.get(sub_category_name=sub_category)
        print('workinggggg..... hhrfhgfv')


        if Product.objects.filter(product_name=title).exists():
            messages.warning(request,'product is already exists')
            return redirect('product:add_product')


        product=Product.objects.create(product_name=title, Category=category_instance, Sub_category=sub_category_instance, price=price, product_description=description)

        for image in images:
            ProductImage.objects.create(product=product,image=image)

        # for values in selected_values.items():
        #     product_attribute=ProductAttribute.objects.create(product=product)
            
        # for key, values in selected_values.items():
        #     for value in values:
        #         product_attribute = ProductAttribute.objects.create(product=product)
        #         print(value, 'agarsah')

        #         attribute = Attributes.objects.get(name=key)
        #         v = Attribute_values.objects.get(attribute=attribute, value=value)
        #         product_attribute.value.add(v)

        #         if value == 'Full':
        #             print('full')
        #             product_attribute.new_price = product.price
        #         elif value == 'quarter':
        #             print('quarter')
        #             product_attribute.new_price = int(product.price) / 4
        #         else:
        #             print('half')
        #             product_attribute.new_price = int(product.price) / 2

        #         print(product_attribute.new_price)

        #         product_attribute.save()

        
        # product_attribute=ProductAttribute.objects.create(product=product)
        # product_attribute.value.set(attribute_values)
        # product_attribute.save()


    return render(request, 'adminpage/products/add_product.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(is_superuser, login_url='adminpage:custom_login')
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

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def edit_image(request):
    if request.method=='POST':
        new_image_file = request.FILES.get('new_image')
        uid=request.POST.get('uid')


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
        image=ProductImage.objects.get(uid=uid)
        image.delete()
        data={'success':'Image deleted successfully'}
        return JsonResponse(data)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def delete_product(request,uid):
    product=Product.objects.get(uid=uid)
    product.is_listed=not product.is_listed
    product.save()
    return redirect('product:products')

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
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


@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def add_product_attributes(request):
    attributes=Attributes.objects.all()
    products=Product.objects.all()
    context={'attributes':attributes, 'products':products}
    if request.method=='POST':
        values=request.POST.getlist('values')
        product=request.POST.get('product')
        price=request.POST.get('price')
        pro=Product.objects.get(product_name=product)
        new=[]
        unique_values = set()
        
        for value in values:
            val = Attribute_values.objects.get(value=value)
            if val in unique_values:
                messages.warning(request, 'Cannot add same attributes.')
                return redirect('product:add_product_attributes')
            elif val.attribute in unique_values:
                messages.warning(request, 'Cannot add same attributes.')
                return redirect('product:add_product_attributes')
            else:
                unique_values.add(val)
                unique_values.add(val.attribute)
                new.append(val)
            product_attribute_exists=ProductAttribute.objects.filter(product=pro,value=val)

        product_attribute=ProductAttribute.objects.create(product=pro, new_price=price)
        for i in new:
            product_attribute.value.add(i)
            product_attribute.save()
        product_attribute.product.is_listed=True
        product_attribute.product.save()
    return render(request, 'adminpage/products/add_product_attributes.html', context)


@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def get_attribute_values(request):
    if request.method=='POST':
        name=json.loads(request.body)['attribute']
        if name=='':
            data={'values':''}
        else:
            attribute=Attributes.objects.get(name=name)
            values=Attribute_values.objects.filter(attribute=attribute)
            data={'values':list(values.values())}
        return JsonResponse(data)
    
@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def get_attributes(request):
    if request.method=='POST':
        data = json.loads(request.body)
        attributes = data.get('attributes', [])
        excluded_attributes = Attributes.objects.exclude(name__in=attributes)
        data={'excluded_attributes':list(excluded_attributes.values())}
        return JsonResponse(data)

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def product_attributes(request):
    product_attributes=ProductAttribute.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(product_attributes, 3)
    page = paginator.get_page(page_number)
    context={'page':page}
    return render(request, 'adminpage/products/product_attributes.html',context)

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def edit_product_attribute(request, uid):
    product_attribute=ProductAttribute.objects.get(uid=uid)
    if request.method=='POST':
        values=request.POST.getlist('values')
        product=request.POST.get('product')
        price=request.POST.get('price')

        product_attribute.value.clear()
        for value in values:
            val = Attribute_values.objects.get(value=value)
            product_attribute.value.add(val)

        product_attribute.new_price=price
        product_attribute.save()
            
    context={'product_attribute':product_attribute, 'attributes':Attributes.objects.all()}
    return render(request, 'adminpage/products/edit_product_attribute.html', context)


@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def add_attribute(request):
    if request.method == 'POST':
        attribute = request.POST.get('attribute')
        if Attributes.objects.filter(name=attribute).exists():
            messages.warning(request, f"Attribute with name '{attribute}' already exists.")
            return redirect('product:add_attribute')
        Attributes.objects.create(name=attribute)
    context = {'attributes':Attributes.objects.all().order_by('name')}
    return render(request,'adminpage/products/add_attribute.html', context)

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def edit_attribute(request, uid):
    if request.method == 'POST':
        new_attribute = request.POST.get('attribute')
        attribute = Attributes.objects.get(uid=uid)
        attribute.name=new_attribute
        attribute.save()
        return redirect('product:add_attribute')
    context = {'attribute':Attributes.objects.get(uid=uid)}
    return render(request,'adminpage/products/edit_attribute.html', context)

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def delete_attribute(reqest, uid):
    attribute = Attributes.objects.get(uid=uid)
    attribute.is_listed=not attribute.is_listed
    # Product.objects.filter(Category=category).update(is_category_listed=category.is_listed)
    attribute.save()
    return redirect('product:add_attribute')

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def attribute_values(request, uid):
    attribute = Attributes.objects.get(uid=uid)
    if request.method == 'POST':
        value = request.POST.get('value')
        if Attribute_values.objects.filter(value = value).exists():
            messages.warning(request, f"Attribute value with name '{value}' already exists.")
            return redirect('product:attribute_values', uid)
        Attribute_values.objects.create(attribute=attribute, value = value)

    context = {'values':attribute.attribute_values.all(), 'attribute':attribute}
    return render(request,'adminpage/products/attribute_values.html', context)

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def edit_attribute_value(request, uid):
    value = Attribute_values.objects.get(uid=uid)
    if request.method == 'POST':
        new_value = request.POST.get('value')
        value.value=new_value
        value.save()
        return redirect('product:attribute_values', value.attribute.uid)

    context={'value':Attribute_values.objects.get(uid=uid)}
    return render(request, 'adminpage/products/edit_attribute_value.html', context)