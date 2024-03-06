from django.shortcuts import render,redirect
from . models import *
from accounts.models import *
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.core.files import File
import razorpay
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponseBadRequest
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files import File as DjangoFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from decouple import config

# Create your views here.

razorpay_client=razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def get_product(request,uid):
    flat=False
    if request.user.is_authenticated:

        flat=True
    product=Product.objects.get(uid=uid)
    images=ProductImage.objects.filter(product=product)
    category=Category.objects.get(uid=product.Category.uid)
    products=Product.objects.filter(Category=category).exclude(uid=product.uid)
    product_attributes=ProductAttribute.objects.filter(product=product)
    d={}
    for i in product_attributes:
        pro_attrbute=i
        break
    for product_attribute in product_attributes:
        for value in product_attribute.value.all():
            key = value.attribute
            if key in d:
                if value not in d[key]:
                    d[key].append(value)
            else:
                d[key] = [value]
    context={'product':product, 'other_images':images, 'flat':flat,'pro_attrbute':pro_attrbute, 'products':products , 'dict':d.items()}
    return render(request, 'products/product.html', context)

def get_value_price(request):
    if request.method=='POST':
        data=json.loads(request.body)
        uid=data['uid']
        value=data['value']
        product=Product.objects.get(uid=uid)
        product_attribute=ProductAttribute.objects.filter(product=product, value__value=value).first()

        data={'new_price':product_attribute.new_price}
        return JsonResponse(data)

def selectvariants(request):
    if request.method=='POST':
        data=json.loads(request.body)
        valueby=data['value']
        key=data['attribute']
        selected_values=data['selected_values']
        product_uid=data['product_uid']
        product=Product.objects.get(uid=product_uid)
        selected=[]
        for key, values in selected_values.items():
            val=Attribute_values.objects.get(value=values)
            selected.append(val.uid)

        try:
            pro_attrbute=ProductAttribute.objects.filter(product=product).filter(value=selected[0]).filter(value=selected[1]).first()
            new=[]
            product_attributes=ProductAttribute.objects.filter(product=product)
            for product_attribute in product_attributes.all():
                for value in product_attribute.value.all():
                    value=Attribute_values.objects.get(value=value)
                    attribute=Attributes.objects.get(name=value.attribute)
                    if attribute.name != key:
                        new.append(value.value)
            data={'values':new,'price':f'₹ {pro_attrbute.new_price}', 'pro_attrbute_uid':pro_attrbute.uid}
            return JsonResponse(data)
        except:
            data={'price':'Currently not available.'}
            return JsonResponse(data) 



def categories(request,uid):
    categories=Category.objects.get(uid=uid)
    sub_categories =Sub_category.objects.filter(category_id=uid)       
    context={'categories':categories, 'sub_categories':sub_categories}
    return render(request, 'products/categories.html',context)


def payment_with_wallet(request,data, uid, discount):
    user=User.objects.get(username=request.user)
    wallet=Wallet.objects.get(user=user)

    if uid:
        quantity=data['quantity']
        sub_total=data['final_price']
        discount_price=sub_total
        unit_price=data['unit_price']
        name=data['name']
        mob=data['mob']
        address=data['address']
        product_name=data['product_name']
        payment_method=data['payment_method']

        product_attribute=ProductAttribute.objects.get(uid=uid)

        if wallet.balance > int(discount_price):
            wallet.balance -= int(discount_price)
            wallet.save()
        else:
            raise ValueError('Insufficient balance in your wallet')

        order=Order.objects.create(user=user,name=name, mob=mob, address=address, total_amount=discount_price, subtotal=sub_total, payment_method=payment_method)
        if discount:
            order.coupon_discount=discount
            order.save()
        ordered_item = Ordered_item.objects.create(order_id=order,ordered_product_name=product_attribute.product.product_name, unit_price=unit_price,qty=quantity)
        ordered_item.image=product_attribute.product
        variants=[]
        for i in product_attribute.value.all():
            variants.append(i.value)
        ordered_item.product_variants=variants
        ordered_item.save()

        Transaction.objects.create(wallet=wallet, amount=discount_price, transaction_type=Transaction.Type.PURCHASED_PRODUCT)

        Payment.objects.create(order=order, payment_method=Payment.PaymentMethod.COD, is_paid=True, amount=discount_price, payment_status=Payment.PaymentStatus.PAID)

        data={'success':order.uid}
        return data
    else:
        cart=Cart.objects.get(user=user)
        cart_items=Cart_item.objects.filter(cart=cart)
        name=data['name']
        mob=data['mob']
        address=data['address']
        sub_total=data['final_price']
        payment_method=data['payment_method']
        discount_price=sub_total

        if wallet.balance > int(discount_price):
            wallet.balance -= int(discount_price)
            wallet.save()
        else:
            raise ValueError('Insufficient balance in your wallet')
        
        order=Order.objects.create(user=user,name=name, mob=mob, address=address, total_amount=discount_price, subtotal=sub_total,payment_method=payment_method)
        if discount:
            order.coupon_discount=discount
            order.save()
        for item in cart_items:
            product_attribute=ProductAttribute.objects.get(uid=item.product_attribute.uid)
            product=Product.objects.get(uid=item.product.uid)
            ordered_item = Ordered_item.objects.create(order_id=order,ordered_product_name=product.product_name,unit_price=product_attribute.new_price, qty=item.qty)
            ordered_item.image=product
            variants=[]
            for i in product_attribute.value.all():
                variants.append(i.value)
            ordered_item.product_variants=variants
            ordered_item.save()

            cart_items.delete()
            cart.save()
        
        Transaction.objects.create(wallet=wallet, amount=discount_price, transaction_type=Transaction.Type.PURCHASED_PRODUCT)
        Payment.objects.create(order=order, payment_method=Payment.PaymentMethod.COD, is_paid=True, amount=discount_price,payment_status=Payment.PaymentStatus.PAID)
        data={'success':order.uid}
        return data



@login_required(login_url='account:login')
def checkout(request, uid=None):
    user=User.objects.get(username=request.user)
    if uid:
        product_attribute=ProductAttribute.objects.get(uid=uid)
        context={'product_attribute':product_attribute, 'addresses':Address.objects.filter(user=user).order_by('-created_at'), 'all_coupons':Coupon.objects.filter(is_expired=False)}

        if request.method=='POST':
            data = json.loads(request.body)
            quantity=data['quantity']
            sub_total=data['final_price']
            discount_price=sub_total
            unit_price=data['unit_price']
            name=data['name']
            mob=data['mob']
            address=data['address']
            product_name=data['product_name']
            payment_method=data['payment_method']

            product=Product.objects.get(uid=product_attribute.product.uid)
            discount=None

            if 'selected_coupon' in data:
                coupon_uid=data['selected_coupon']
                discount_price=data['discount']
                coupon=Coupon.objects.get(uid=coupon_uid)
                discount=coupon.discount_price
                discount_price = int(sub_total) - discount
                if coupon.is_expired==False and coupon.expire_date>=timezone.now():
                    coupon.no_of_coupons-=1
                    coupon.save()
                    cart=Cart.objects.get(user=user)
                    cart.applied_coupon=coupon
                    cart.save()
                else:
                    data={'expired':'Coupon expired'}
                    return JsonResponse(data)
            if data['payment_method']=='Payment':
                datas={'quantity':quantity,'sub_total':sub_total,'discount_price':discount_price, 'unit_price':unit_price,'name':name, 'mob':mob, 'address':address, 'product_uid':uid, 'discount':discount, 'user':user.id, 'payment_method':payment_method}
                serialized_data = json.dumps(datas)
                cache.set('data',serialized_data)
                currency = 'INR'
                amount = int(discount_price) * 100  

                try:
                    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
                    razorpay_order_id = razorpay_order['id']
                    callback_url = 'https://elbin.site/products/paymenthandler/' + str(amount/100)

                    context = {
                        'name': name,
                        'mob': mob,
                        'address': address,
                        'total_amount': discount_price,
                        'razorpay_order_id': razorpay_order_id,
                        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
                        'razorpay_amount': amount,
                        'currency': currency,
                        'callback_url': callback_url,
                    }

                    return JsonResponse(context)
                except Exception as e:
                    return JsonResponse({'error': 'Internal Server Error'}, status=500)
            elif data['payment_method']=='Wallet':
                try:
                    message=payment_with_wallet(request,data, uid, discount)
                    return JsonResponse({'url':'/products/order_success/'+str(message['success'])})
                except ValueError as e:
                    return JsonResponse({'fail': str(e)})
                
            else:
                order=Order.objects.create(user=user,name=name, mob=mob, address=address, total_amount=discount_price, subtotal=sub_total, payment_method=payment_method)
                if discount:
                    order.coupon_discount=discount
                    order.save()
                ordered_item = Ordered_item.objects.create(order_id=order,ordered_product_name=product.product_name,unit_price=product_attribute.new_price, qty=quantity)
                ordered_item.image=product
                variants=[]
                for i in product_attribute.value.all():
                    variants.append(i.value)
                ordered_item.product_variants=variants
                    
                ordered_item.save()

                Payment.objects.create(order=order, payment_method=Payment.PaymentMethod.COD, is_paid=False, amount=discount_price)
                
                return JsonResponse({'url':'/products/order_success/'+str(order.uid)})
    else:
        cart=Cart.objects.get(user=user)
        cart_items=Cart_item.objects.filter(cart=cart)
        len=cart_items.__len__()
        if request.method=='POST':
            data = json.loads(request.body)
            name=data['name']
            mob=data['mob']
            address=data['address']
            sub_total=data['final_price']
            payment_method=data['payment_method']
            discount_price=sub_total

            discount=None

            if 'selected_coupon'in data:
                coupon_uid=data['selected_coupon']
                discount_price=cart.total - int(data['discount'])
                coupon=Coupon.objects.get(uid=coupon_uid)
                discount=coupon.discount_price
                if coupon.is_expired==False:
                    coupon.no_of_coupons-=1
                    coupon.save()
                    cart.applied_coupon=coupon
                    cart.save()
                else:
                    data={'expired':'Coupon expired'}
                    return JsonResponse(data)
                
            if data['payment_method']=='Payment':
                datas={'sub_total':sub_total,'discount_price':discount_price,'name':name, 'mob':mob, 'address':address, 'discount':discount, 'user':user.id, 'payment_method':payment_method}
                serialized_data = json.dumps(datas)
                cache.set('data',serialized_data)
                currency = 'INR'
                amount = int(discount_price) * 100  

                try:
                    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
                    razorpay_order_id = razorpay_order['id']
                    callback_url = "http://" + "127.0.0.1:8000" + '/products/paymenthandler/'+str(amount/100)

                    context = {
                        'name': name,
                        'mob': mob,
                        'address': address,
                        'total_amount': discount_price,
                        'razorpay_order_id': razorpay_order_id,
                        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
                        'razorpay_amount': amount,
                        'currency': currency,
                        'callback_url': callback_url,
                    }

                    return JsonResponse(context)
                except Exception as e:
                    return JsonResponse({'error': 'Internal Server Error'}, status=500)
                
            elif data['payment_method']=='Wallet':
                try:
                    message=payment_with_wallet(request,data, uid, discount)
                    return JsonResponse({'url':'/products/order_success/'+str(message['success'])})
                except ValueError as e:
                    return JsonResponse({'fail': str(e)})

            else:
                order=Order.objects.create(user=user,name=name, mob=mob, address=address, total_amount=discount_price, subtotal=sub_total,payment_method=payment_method)
                if discount:
                    order.coupon_discount=discount
                    order.save()
                for item in cart_items:
                    product_attribute=ProductAttribute.objects.get(uid=item.product_attribute.uid)
                    product=Product.objects.get(uid=item.product.uid)
                    ordered_item = Ordered_item.objects.create(order_id=order,ordered_product_name=product.product_name,unit_price=product_attribute.new_price, qty=item.qty)
                    ordered_item.image=product
                    variants=[]
                    for i in product_attribute.value.all():
                        variants.append(i.value)
                    ordered_item.product_variants=variants
                    ordered_item.save()
                cart_items.delete()
                cart.save()
                Payment.objects.create(order=order, payment_method=Payment.PaymentMethod.COD, is_paid=False, amount=discount_price)
                return JsonResponse({'url':'/products/order_success/'+str(order.uid)})
        
        context={'cart_items':cart_items,'cart':cart,'len':len, 'addresses':Address.objects.filter(user=user).order_by('-created_at'),'all_coupons':Coupon.objects.filter(is_expired=False)}
    return render(request, 'products/buynow.html', context)

@csrf_exempt
def paymenthandler(request, amount):

    serialized_data = cache.get('data')
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                try: 
                    amount = int(Decimal(amount) * 100)
                    # capture the payemt
                    if serialized_data is not None:
                        if 'product_uid' in serialized_data:
                            data = json.loads(serialized_data)
                            quantity=data['quantity']
                            sub_total=data['sub_total']
                            unit_price=data['unit_price']
                            name=data['name']
                            mob=data['mob']
                            address=data['address']
                            product_uid=data['product_uid']
                            discount=data['discount']
                            discount_price=data['discount_price']
                            user=data['user']
                            payment_method=data['payment_method']

                            product_attribute=ProductAttribute.objects.get(uid=product_uid)

                            order_user=User.objects.get(id=user)
                            order=Order.objects.create(user=order_user,name=name, mob=mob, address=address, total_amount=discount_price, subtotal=sub_total, payment_method=payment_method)
                            if discount:
                                order.coupon_discount=discount
                                order.save()
                            ordered_item = Ordered_item.objects.create(order_id=order,ordered_product_name=product_attribute.product.product_name, unit_price=unit_price,qty=quantity)
                            ordered_item.image=product_attribute.product
                            variants=[]
                            for i in product_attribute.value.all():
                                variants.append(i.value)
                            ordered_item.product_variants=variants
                            ordered_item.save()
                
                        else:
                            data = json.loads(serialized_data)
                            sub_total=data['sub_total']
                            name=data['name']
                            mob=data['mob']
                            address=data['address']
                            discount=data['discount']
                            discount_price=data['discount_price']
                            user=data['user']
                            payment_method=data['payment_method']

                            order_user=User.objects.get(id=user)
                            cart=Cart.objects.get(user=order_user)
                            cart_items=Cart_item.objects.filter(cart=cart)

                            order=Order.objects.create(user=order_user,name=name, mob=mob, address=address, total_amount=discount_price, subtotal=sub_total,payment_method=payment_method)

                            if discount:
                                order.coupon_discount=discount
                                order.save()

                            for item in cart_items:
                                product_attribute=ProductAttribute.objects.get(uid=item.product_attribute.uid)
                                product=Product.objects.get(uid=item.product.uid)

                                ordered_item = Ordered_item.objects.create(order_id=order,ordered_product_name=product.product_name,unit_price=product_attribute.new_price, qty=item.qty)
                                ordered_item.image=product
                                variants=[]
                                for i in product_attribute.value.all():
                                    variants.append(i.value)
                                ordered_item.product_variants=variants
                                ordered_item.save()

                            cart_items.delete()
                            cart.save()

                    Payment.objects.create(order=order, payment_method=Payment.PaymentMethod.PAYMENT, is_paid=True,payment_status=Payment.PaymentStatus.PAID, razorpay_order_id=razorpay_order_id, rarzorpay_payment_id=payment_id, razorpay_payment_signature=signature, amount=discount_price)
                    razorpay_client.payment.capture(payment_id, amount)

                    return redirect('products:order_success',order.uid)
                except:
                    return render(request, 'paymentfail.html')
            else:
                return render(request, 'paymentfail.html')
        except:
            return redirect('products:cart_checkout')
    else:
        return redirect('account:login')




@login_required(login_url='account:login')
def order_success(request, uid):
    order=Order.objects.get(uid=uid)
    context={'order':order}
    return render(request, 'products/order_success.html', context)


def clear_search_from_session(request):
    if request.method == 'POST':
        if 'search_value' in request.session:
            del request.session['search_value']
            return JsonResponse({'message': 'Search value cleared from session'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
    
def search_view(request):
    val=1
    serialized_data = []
    if request.method == 'GET':
        search = request.GET.get('search')
        searchdata = json.dumps(search)
        request.session['search_value'] = search
        products = Product.objects.filter(is_listed = True).filter(product_name__icontains = search)
    page_number = request.GET.get('page')
    paginator = Paginator(products, 3)
    page = paginator.get_page(page_number)
    # Redirect to shop view with search query and filter option
    context = {'page': page, 'categories': Category.objects.all(), 'val':val, 'serialized_data': serialized_data, 'search':searchdata}
    return render(request, 'shop.html', context)

def shop_page(request):
    products = Product.objects.filter(is_listed=True)
    val=1
    serialized_data = []
    searchdata =None

    if request.method == 'POST':
        search = request.POST.get('search')
        print(search)
        products = Product.objects.filter(is_listed = True).filter(product_name__icontains = search)

    if request.method=='GET':
        search_shop = request.GET.get('search') 
        if search_shop and search_shop is not None:
            products = Product.objects.filter(is_listed = True).filter(product_name__icontains = search_shop)
            print(products)
        # search_query = request.GET.get('search', '')
        filter_value = request.GET.getlist('category')
        sort_value = request.GET.get('sortbyprice')

        # if search_query:
        #     products = products.filter(name__icontains=search_query)

        if filter_value:
            products= products.filter(Category__category_name__in=filter_value)
            serialized_data = json.dumps(filter_value)
        if sort_value:
            if sort_value == '1':
                products = products.order_by('price')
                val ='1'
            elif sort_value == '2':
                val = '2'
                products = products.order_by('-price')

    page_number = request.GET.get('page')
    paginator = Paginator(products, 3)
    page = paginator.get_page(page_number)

    context = {'page': page, 'categories': Category.objects.all(), 'val':val, 'serialized_data': serialized_data}
    if search_shop and search_shop is not None:
        context['search'] =search_shop
    if searchdata is not None:
        context['search'] = searchdata
    return render(request, 'shop.html', context)


def apply_coupon(request):
    if request.method=='POST':
        data=json.loads(request.body)
        coupon_uid=data['coupon_uid']
        total=data['total']
        coupon=Coupon.objects.get(uid=coupon_uid,)
        if coupon.is_expired==True or coupon.no_of_coupons==0:
            data = {'fail':'Coupon Expired'}
            return JsonResponse(data)
        elif int(total)>=coupon.minimum_amount:
            discount=coupon.discount_price
            data={'success':'coupon applied', 'discount':discount}
            return JsonResponse(data)
        else:
            data = {'fail': f'Coupon is valid for orders greater than {coupon.minimum_amount} rupees  '}
        return JsonResponse(data)