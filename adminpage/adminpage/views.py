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

from django.db.models import Prefetch
from collections import defaultdict
from collections import Counter

from django.db.models import Sum
from django.utils import timezone
import calendar
from django.db.models import Q

import pandas as pd
from io import BytesIO
from django.http  import HttpResponse
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
            return render(request,'adminpage/adminpage/login.html')
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


def monthly_earnings():
    current_year = timezone.now().year
    current_month = timezone.now().month


    # Get the number of days in the current month
    _, num_days = calendar.monthrange(current_year, current_month)

    # Calculate the start and end dates for the current month
    start_date = timezone.datetime(current_year, current_month, 1)
    end_date = timezone.datetime(current_year, current_month, num_days, 23, 59, 59)

    # Calculate the total earnings for the current month
    monthly_earnings = Order.objects.filter(order_status=Order.OrderStatus.DELIVERED).filter(created_at__range=(start_date, end_date)).aggregate(total_earnings=Sum('total_amount'))['total_earnings'] or 0
    return monthly_earnings



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def home(request):
    orders=Order.objects.filter(order_status=Order.OrderStatus.DELIVERED)
    count = orders.__len__()
    revenue = Order.objects.filter(order_status=Order.OrderStatus.DELIVERED).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0

    chart_month = []
    new_users = []
    orders_count= []
    for month in range(1,13):
        c = 0
        user_count = 0
        order_c = 0
        for item in Ordered_item.objects.filter(order_id__order_status=Order.OrderStatus.DELIVERED):
            if item.created_at.month == month:
                c += item.qty
                order_c +=1
                
        chart_month.append(c)
        for user in Profile.objects.all():
            if user.user.date_joined.month == month:
                user_count +=1
        new_users.append(user_count)

        for order in Order.objects.filter(order_status=Order.OrderStatus.DELIVERED):
            if order.created_at.month == month:
                order_c +=1
        orders_count.append(order_c)

    all_orders = Order.objects.all().order_by('-created_at')

    if request.method == 'GET':
        date = request.GET.get('date')
        order_filter = request.GET.get('order_filter')

        if order_filter and order_filter!= 'All':
            all_orders = all_orders.filter( payment__payment_status = order_filter)

        if date:
            date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
            date_datetime = datetime.strptime(str(date), '%Y-%m-%d')
            all_orders = all_orders.filter(created_at__date=date_datetime)
   
   
    delivered_orders = Order.objects.filter(order_status=Order.OrderStatus.DELIVERED)


    delivered_orders_with_items = delivered_orders.prefetch_related(
        Prefetch('ordered_items', queryset=Ordered_item.objects.select_related('order_id'))
    )

    delivered_product_attributes = []

    for order in delivered_orders_with_items:
        for item in order.ordered_items.all():
            # if item.product_variants:
            #     v = []
            #     for variant in item.product_variants:
            #         for i in item.image.product_attributes.all():
            #             for val in i.value.all():
            #                 if val.value == variant:
            #                     v.append(val)
            #     print(set(v),'variant ', v)
            #     v =list(set(v))
            #     print(v)
            #     product_attribute = ProductAttribute.objects.filter(product=item.image).filter(value = v[0]).filter(value = v[1]).first()
            #     print(product_attribute, 'productattribute')
            delivered_product_attributes.append(item.image)

    product_attribute_counter = Counter(delivered_product_attributes)

    sorted_product_attributes = sorted(product_attribute_counter.items(), key=lambda x: x[1], reverse=True)

    monthly_earning = monthly_earnings()
                
        
    products_count = Product.objects.all().__len__
    categories_count = Category.objects.all().__len__
    payment_statuses = Payment.PaymentStatus.choices
    context={'revenue':revenue, 'count':count, 'orders':all_orders,'date':date,'order_filter':order_filter, 'users':Profile.objects.all().order_by('-created_at'), 'month' : chart_month, 'new_users':new_users, 'orders_count':orders_count,'payment_statuses':payment_statuses, 'sorted_product_attributes':sorted_product_attributes, 'monthly_earning':monthly_earning, 'products_count':products_count, 'categories_count':categories_count}
    return render(request,'adminpage/adminpage/home.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def users(request):
    users=User.objects.all()
    profile=Profile.objects.filter(user__in=users).order_by('user__username')
    context={}
    if request.method == 'GET':
        search = request.GET.get('search_user')
        status = request.GET.get('status')
        if search:
            profile = profile.filter(user__first_name__istartswith=search).order_by('user__username')
            context['search'] = search
        if status == 'Active':
            profile = profile.filter(user__is_active=True).order_by('user__username')
            context['status'] = status
        if status == 'Disabled':
            profile = profile.filter(user__is_active=False).order_by('user__username')
            context['status'] = status

    context['profiles'] = profile
    return render(request, 'adminpage/adminpage/users.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def block_user(request, id):
    user=User.objects.get(id=id)
    profile=Profile.objects.get(user=user)
    profile.block= not profile.block
    user.is_active=not user.is_active
    profile.save()
    user.save()
    return redirect('adminpage:users')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def user_details(request,id):
    user=User.objects.get(id=id)
    profile=Profile.objects.get(user=user)
    orders=Order.objects.filter(user=user).exclude(order_status=Order.OrderStatus.CANCELLED_BY_ADMIN).exclude(order_status=Order.OrderStatus.CANCELLED)
    context={'profile':profile, 'orders':orders}
    return render(request, 'adminpage/adminpage/user_details.html',context)


@user_passes_test(is_superuser, login_url='adminpage:custom_login')
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

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def delete_banner(request, uid):
    banner=Banner.objects.get(uid=uid)
    banner.delete()
    return redirect('adminpage:banner')

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def orders(request):
    orders=Order.objects.all().order_by('-created_at')
    context={'order':Order}
    if request.method == 'GET':
        status = request.GET.get('status')
        if status and not status == 'All status':
            orders = orders.filter(order_status = status)
            context['orders'] = orders
            context['selected_status'] = status
    context['orders'] = orders
    return render(request, 'adminpage/order/order.html', context)

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def order_details(request, uid):
    order=Order.objects.get(uid=uid)
    order_statuses = [status[0] for status in Order.OrderStatus.choices]
    ordered_items=Ordered_item.objects.filter(order_id=order)

    if request.method=='POST':
        status=request.POST.get('order_status')
        order.order_status=status
        payment = order.payment.first()
        if (status == 'Cancelled' or status == 'Cancelled by admin') and order.payment_method != 'COD':
            payment.payment_status = Payment.PaymentStatus.REFUND
            payment.save()
            user = User.objects.get(username = order.user)
            wallet = Wallet.objects.get(user = user)
            Transaction.objects.create(wallet = wallet, amount = order.total_amount ,transaction_type = Transaction.Type.DEPOSIT)
            wallet.balance+=order.total_amount
            wallet.save()
        order.save()
        return redirect('adminpage:orders')
    context={'order':order, 'order_statuses':order_statuses, 'ordered_items':ordered_items}
    return render(request, 'adminpage/order/order_details.html', context)

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def approve_cancel_request(request,uid):
    order=Order.objects.get(uid=uid)
    order.order_status=Order.OrderStatus.CANCELLED
    payment = order.payment.first()
    if order.payment_method !='COD':
        payment.payment_status = Payment.PaymentStatus.REFUND
        payment.save()
        user=User.objects.get(username=order.user)
        wallet=Wallet.objects.get(user=user)
        wallet.balance+=order.total_amount
        transaction=Transaction.objects.create(wallet=wallet, amount=order.total_amount, transaction_type=Transaction.Type.DEPOSIT)
        wallet.save()
    order.save()
    return redirect('adminpage:orders')


@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def coupons(request):
    context={'all_coupons':Coupon.objects.all().order_by('coupon_code')}
    return render(request, 'adminpage/adminpage/coupons.html', context)

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
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


@user_passes_test(is_superuser, login_url='adminpage:custom_login')
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

@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def activate_coupon(request, uid):
    coupon=Coupon.objects.get(uid=uid)
    coupon.is_expired= not coupon.is_expired
    coupon.save()
    return redirect('adminpage:coupons')


@user_passes_test(is_superuser, login_url='adminpage:custom_login')
def sales_report(request):
    items = Ordered_item.objects.filter(order_id__order_status=Order.OrderStatus.DELIVERED)
    context = {'items': items}
    return render(request, 'adminpage/adminpage/sales_report.html', context)


def export_data_to_excel(request):
    objs = Ordered_item.objects.all()
    orders = Order.objects.all()
    
    data = []

    for obj in objs:
        data.append({
            "Order ID": obj.order_id.uid,
            "Item ID": obj.uid,
            "Product": obj.ordered_product_name,
            "Product Variant": ', '.join(obj.product_variants),
            "Quantity": obj.qty,
            "Price": obj.price,
            "Payment Method": obj.order_id.payment_method,
            "Address": obj.order_id.address,
            "Mobile": obj.order_id.mob,
            "Total": obj.order_id.total_amount,
            "Paid": obj.order_id.payment.first().payment_status,
            "Order Status": obj.order_id.order_status,
        })

    overall_revenue = sum(order.total_amount for order in orders)
    overall_data = {
        "Overall Revenue": overall_revenue,
        
    }

    df_orders = pd.DataFrame(data)
    df_overall = pd.DataFrame([overall_data])

    total_revenue = Order.objects.filter(order_status=Order.OrderStatus.DELIVERED).aggregate(Sum('total_amount'))['total_amount__sum']
    total_count = Order.objects.filter(order_status=Order.OrderStatus.DELIVERED).count()
    product_count = Product.objects.all().count()
    category_count = Category.objects.all().count()
    if total_count > 0:
        monthly_revenue = total_revenue / total_count
    else:
        monthly_revenue = 0



    if total_revenue is None:
        total_revenue = 0
    if total_count is None:
        total_count = 0
    if product_count is None:
        product_count = 0
    if category_count is None:
        category_count = 0

    overall_combined_data = {
        "Overall Revenue": total_revenue,
        "Total Products Available": product_count,
        "Overall Categories": category_count,
        "Monthly Income": monthly_revenue,
    }


    df_overall_combined = pd.DataFrame([overall_combined_data])

    output_buffer = BytesIO()
    with pd.ExcelWriter(output_buffer, engine='xlsxwriter') as writer:
        df_orders.to_excel(writer, sheet_name='Orders', index=False)

        worksheet_orders = writer.sheets['Orders']
        for i, col in enumerate(df_orders.columns):
            max_len = max(df_orders[col].astype(str).apply(len).max(), len(col))
            worksheet_orders.set_column(i, i, max_len)
       

        df_overall_combined = pd.DataFrame([overall_combined_data])
        df_overall_combined.to_excel(writer, sheet_name='Overall',startcol = 2,  index=False)
        start_row_monthly_data = len(df_overall_combined) + 5  
        start_col_monthly_data = len(df_overall_combined.columns) + 2
        df_monthly_data = pd.DataFrame({
            "Months": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            "Sales": [100, 150, 200, 120, 180, 250, 300, 200, 180, 220, 280, 320],
            "Products": [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160],
            "Visitors": [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600],
        })
        df_monthly_data.to_excel(writer, sheet_name='Overall',  startcol=start_col_monthly_data + 5 , index=False)
        worksheet = writer.sheets['Overall']
        for i, col in enumerate(df_overall_combined.columns):
            max_len = max(df_overall_combined[col].astype(str).apply(len).max(), len(col))
            worksheet.set_column(i + 2, i + 2, max_len) 

        for i, col in enumerate(df_monthly_data.columns):
            max_len = max(df_monthly_data[col].astype(str).apply(len).max(), len(col))
            worksheet.set_column(start_col_monthly_data + i, start_col_monthly_data + i, max_len)  


    output_buffer.seek(0)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_report.xlsx'
    response.write(output_buffer.getvalue())

    return response