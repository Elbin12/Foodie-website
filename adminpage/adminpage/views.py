from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import *
from products.models import *
from .models import *
from home.models import Banner
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminpage:home')
        else:
            messages.error(request, 'You are not admin')
            return render(request,'adminpage/login.html')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username, password=password)
        if user is not None and user.is_authenticated:
            if not user.is_superuser:
                messages.error(request, 'You are not admin')
                return redirect('adminpage:custom_login')       
            elif user.is_superuser:
                login(request,user)
                return redirect('adminpage:home')
        else:
            messages.error(request, 'Enter valid username and password')
            return redirect('adminpage:custom_login')
    return render(request, 'adminpage/adminpage/login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('adminpage:custom_login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def home(request):
    orders=Order.objects.filter(order_status=Order.OrderStatus.DELIVERED)
    revenue = Order.objects.filter(order_status=Order.OrderStatus.DELIVERED).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
    print(revenue)
    context={'revenue':revenue, 'count':orders.__len__, 'orders':Order.objects.all().order_by('-created_at')}
    return render(request,'adminpage/adminpage/home.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def users(request):
    users=User.objects.all()
    profile=Profile.objects.filter(user__in=users).order_by('user__username')
    context={'profiles':profile}
    return render(request, 'adminpage/adminpage/users.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def block_user(request, id):
    user=User.objects.get(id=id)
    profile=Profile.objects.get(user=user)
    print(profile.user.username,user.is_active,profile.block,'none')
    profile.block= not profile.block
    user.is_active=not user.is_active
    profile.save()
    user.save()
    return redirect('adminpage:users')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminpage:custom_login')
def user_details(request,id):
    user=User.objects.get(id=id)
    profile=Profile.objects.get(user=user)
    orders=Order.objects.filter(user=user).exclude(order_status=Order.OrderStatus.CANCELLED_BY_ADMIN).exclude(order_status=Order.OrderStatus.CANCELLED)
    context={'profile':profile, 'orders':orders}
    return render(request, 'adminpage/adminpage/user_details.html',context)



def banner(request):
    banners=Banner.objects.all().order_by('order')
    context={'banners':banners}
    if request.method=='POST':
        banner_image=request.FILES.get('banner')
        order=request.POST.get('order')
        if Banner.objects.filter(image=banner_image).exists():
            messages.warning(request, 'image already uploaded')
            return redirect('adminpage:banner')
        else:
            Banner.objects.create(image=banner_image, order=order)
    return render(request, 'adminpage/adminpage/banners.html',context)


def delete_banner(request, uid):
    banner=Banner.objects.get(uid=uid)
    banner.delete()
    return redirect('adminpage:banner')


def orders(request):
    orders=Order.objects.all().order_by('-created_at')
    context={'orders':orders}
    return render(request, 'adminpage/order/order.html', context)

def order_details(request, uid):
    order=Order.objects.get(uid=uid)
    order_statuses = [status[0] for status in Order.OrderStatus.choices]
    ordered_items=Ordered_item.objects.filter(order_id=order)

    if request.method=='POST':
        status=request.POST.get('order_status')
        order.order_status=status
        order.save()
        if (status == 'Cancelled' or status == 'Cancelled by admin') and order.payment_method != 'COD':
            print(status)
            user = User.objects.get(username = order.user)
            wallet = Wallet.objects.get(user = user)
            Transaction.objects.create(wallet = wallet, amount = order.total_amount ,transaction_type = Transaction.Type.DEPOSIT)
            wallet.balance+=order.total_amount
            wallet.save()
        
        return redirect('adminpage:orders')
    context={'order':order, 'order_statuses':order_statuses, 'ordered_items':ordered_items}
    return render(request, 'adminpage/order/order_details.html', context)


def approve_cancel_request(request,uid):
    order=Order.objects.get(uid=uid)
    order.order_status=Order.OrderStatus.CANCELLED
    if order.payment_method !='COD':
        print('ag', order.user,'ioiufdyfuilo;p')
        user=User.objects.get(username=order.user)
        wallet=Wallet.objects.get(user=user)
        wallet.balance+=order.total_amount
        transaction=Transaction.objects.create(wallet=wallet, amount=order.total_amount, transaction_type=Transaction.Type.DEPOSIT)
        wallet.save()
    order.save()
    return redirect('adminpage:orders')



def coupons(request):
    context={'all_coupons':Coupon.objects.all().order_by('coupon_code')}
    return render(request, 'adminpage/adminpage/coupons.html', context)


def add_coupon (request):
    if request.method=='POST':
        coupon_code=request.POST.get('coupon_code')
        discount_price=request.POST.get('discount_price')
        min_amount=request.POST.get('min_amount')
        no_of_coupons=request.POST.get('no_of_coupons')
        expire_date=request.POST.get('expire_date')

        expire_date = timezone.now() + timedelta(int(expire_date))
        Coupon.objects.create(coupon_code=coupon_code, discount_price=discount_price, minimum_amount=min_amount, no_of_coupons=no_of_coupons, expire_date=expire_date)
        return redirect('adminpage:coupons')

    return render(request, 'adminpage/adminpage/add_coupon.html')


def edit_coupon(request, uid):
    coupon=Coupon.objects.get(uid=uid)
    context={'coupon':coupon}
    if request.method=='POST':
        coupon_code=request.POST.get('coupon_code')
        discount_price=request.POST.get('discount_price')
        min_amount=request.POST.get('min_amount')
        no_of_coupons=request.POST.get('no_of_coupons')
        expire_date=request.POST.get('expire_date')

        coupon.coupon_code=coupon_code
        coupon.discount_price=discount_price
        coupon.minimum_amount=min_amount
        coupon.no_of_coupons=no_of_coupons
        coupon.expire_date = timezone.now() + timedelta(int(expire_date))
        coupon.save()
        
        return redirect('adminpage:coupons')
    return render(request, 'adminpage/adminpage/edit_coupon.html', context)


def activate_coupon(request, uid):
    coupon=Coupon.objects.get(uid=uid)
    coupon.is_expired= not coupon.is_expired
    print(coupon.is_expired, coupon, 'ijodf')
    coupon.save()
    print(coupon.is_expired, coupon, 'ijodf')
    return redirect('adminpage:coupons')