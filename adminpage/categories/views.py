from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Profile
from products.models import Category,Sub_category,Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import user_passes_test


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def add_category(request):
    categories=Category.objects.all().order_by('category_name')
    context={'categories':categories}
    if request.method=="POST":
        category=request.POST.get('category')
        category_exists=Category.objects.filter(category_name=category)
        if category_exists.exists():
            messages.warning(request,'Category already exists')
            return redirect('category:add_category')
        else:
            Category.objects.create(category_name=category)
            return redirect('category:add_category')
    return render(request, 'adminpage/categories/add_category.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def edit_category(request,uid):
    category=Category.objects.get(uid=uid)
    context={'category':category}
    if request.method=='POST':
        new_category=request.POST.get('category')
        image=request.FILES.get('image')

        category.category_name=new_category
        category.category_image=image
        category.save()
        return redirect('category:add_category')

    return render(request, 'adminpage/categories/edit_category.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def delete_category(request,uid):
    category=Category.objects.get(uid=uid)
    print(category)
    category.is_listed=not category.is_listed
    Product.objects.filter(Category=category).update(is_category_listed=category.is_listed)
    category.save()
    return redirect('category:add_category')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def add_sub_category(request,uid):
    category_instance=Category.objects.get(uid=uid)
    categories=Category.objects.all()
    sub_categories=Sub_category.objects.filter(category=category_instance)
    context={'sub_categories':sub_categories,'category':category_instance, 'categories':categories}
    
    if request.method=='POST':
        sub_category=request.POST.get('sub_category')

        sub_category_exists=Sub_category.objects.filter(sub_category_name=sub_category)
        if sub_category_exists.exists():
            messages.warning(request,'Sub category already exists')
            return redirect('category:add_sub_category',uid)
        else:
            Sub_category.objects.create(category=category_instance,sub_category_name=sub_category)
            return redirect('category:add_sub_category',uid)
    return render(request, 'adminpage/categories/add_sub_category.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def edit_subcategory(request,uid):
    sub_category=Sub_category.objects.get(uid=uid)
    category=Category.objects.get(sub_categories=sub_category)
    context={'sub_category':sub_category}
    if request.method=='POST':
        new_sub_category=request.POST.get('sub_category')
        sub_category.sub_category_name=new_sub_category
        sub_category.save()
        return redirect('category:add_sub_category',category.uid)
    return render(request, 'adminpage/categories/edit_subcategory.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def delete_sub_category(request,uid):
    sub_category=Sub_category.objects.get(uid=uid)
    category=Category.objects.get(sub_categories=sub_category)
    context={'sub_category':sub_category}
    if request.method=='POST':
        sub_category.delete()
        return redirect('category:add_sub_category',category.uid)
    return render(request, 'adminpage/categories/delete_sub_category.html',context)

