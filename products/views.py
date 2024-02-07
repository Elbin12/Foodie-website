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


# Create your views here.

razorpay_client=razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def get_product(request,uid):
    flat=False
    if request.user.is_authenticated:
        print(request.user)
        flat=True
    product=Product.objects.get(uid=uid)
    images=ProductImage.objects.filter(product=product)
    category=Category.objects.get(uid=product.Category.uid)
    products=Product.objects.filter(Category=category).exclude(uid=product.uid)
    product_attributes=ProductAttribute.objects.filter(product=product)
    values_list = []
    for product_attribute in product_attributes:
        values_list.extend(product_attribute.value.all())
    print(values_list)
    context={'product':product, 'other_images':images, 'flat':flat, 'products':products ,'values':values_list}
    return render(request, 'products/product.html', context)

def get_value_price(request):
    if request.method=='POST':
        data=json.loads(request.body)
        uid=data['uid']
        value=data['value']
        product=Product.objects.get(uid=uid)
        product_attribute=ProductAttribute.objects.filter(product=product, value__value=value).first()
        print(product_attribute.new_price)

        data={'new_price':product_attribute.new_price}
        return JsonResponse(data)



def categories(request,uid):
    categories=Category.objects.get(uid=uid)
    sub_categories =Sub_category.objects.filter(category_id=uid)       
    context={'categories':categories, 'sub_categories':sub_categories}
    return render(request, 'products/categories.html',context)


def payment_with_wallet(request,data, uid, discount):
    print('bjnklm;', uid)
    user=User.objects.get(username=request.user)
    wallet=Wallet.objects.get(user=user)

    if uid:
        print('bkjln', uid)
        quantity=data['quantity']
        sub_total=data['final_price']
        discount_price=sub_total
        unit_price=data['unit_price']
        name=data['name']
        mob=data['mob']
        address=data['address']
        product_name=data['product_name']
        payment_method=data['payment_method']

        product=Product.objects.get(uid=uid)
        product_image=product.product_images.first()
        product_image_file = File(product_image.image.file)

        order=Order.objects.create(user=user,name=name, mob=mob, address=address, total_amount=discount_price, subtotal=sub_total, payment_method=payment_method)
        if discount:
            order.coupon_discount=discount
            order.save()
        Ordered_item.objects.create(order_id=order,ordered_product_name=product_name, unit_price=unit_price,qty=quantity, image=product_image_file)

        if wallet.balance > int(discount_price):
            wallet.balance -= int(discount_price)
            wallet.save()
        else:
            raise ValueError('Insufficient balance in your wallet')

        Transaction.objects.create(wallet=wallet, amount=discount_price, transaction_type=Transaction.Type.PURCHASED_PRODUCT)

        Payment.objects.create(order=order, payment_method=Payment.PaymentMethod.COD, is_paid=False, amount=discount_price)
        data={'success':order.uid}
        return data





@login_required(login_url='account:login')
def checkout(request, uid=None):
    user=User.objects.get(username=request.user)
    if uid:
        product=Product.objects.get(uid=uid)
        context={'product':product, 'addresses':Address.objects.filter(user=user).order_by('-created_at'), 'all_coupons':Coupon.objects.filter(is_expired=False)}

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
            print(payment_method, 'ijohgaszgfdf')
            product_image=product.product_images.first()
            product_image_file = File(product_image.image.file)
            print(product_image_file, product_image)

            discount=None

            if 'selected_coupon' in data:
                coupon_uid=data['selected_coupon']
                discount_price=data['discount']
                coupon=Coupon.objects.get(uid=coupon_uid)
                discount=coupon.discount_price
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
                print('payment function called ')
                datas={'quantity':quantity,'sub_total':sub_total,'discount_price':discount_price, 'unit_price':unit_price,'name':name, 'mob':mob, 'address':address, 'product_uid':uid, 'discount':discount, 'user':user.id, 'payment_method':payment_method}
                serialized_data = json.dumps(datas)
                print(serialized_data)
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
                    print('Error creating Razorpay order:', str(e))
                    return JsonResponse({'error': 'Internal Server Error'}, status=500)
            elif data['payment_method']=='Wallet':
                print('bibnokl',uid)
                try:
                    message=payment_with_wallet(request,data, uid, discount)
                    print('ijnjnj',message)
                    print('success',message['success'])
                    return JsonResponse({'url':'/products/order_success/'+str(message['success'])})
                except ValueError as e:
                    return JsonResponse({'fail': str(e)})
                
            else:
                order=Order.objects.create(user=user,name=name, mob=mob, address=address, total_amount=discount_price, subtotal=sub_total, payment_method=payment_method)
                if discount:
                    order.coupon_discount=discount
                    order.save()
                Ordered_item.objects.create(order_id=order,ordered_product_name=product_name, unit_price=unit_price,qty=quantity, image=product_image_file)

                Payment.objects.create(order=order, payment_method=Payment.PaymentMethod.COD, is_paid=False, amount=discount_price)
                
                print(sub_total, address)
                
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
                discount_price=data['discount']
                coupon=Coupon.objects.get(uid=coupon_uid)
                discount=coupon.discount_price
                if coupon.is_expired==False:
                    coupon.no_of_coupons-=1
                    coupon.save()
                    print(cart)
                    cart.applied_coupon=coupon
                    print(cart,cart.applied_coupon)
                    cart.save()
                else:
                    data={'expired':'Coupon expired'}
                    return JsonResponse(data)
                
            if data['payment_method']=='Payment':
                print('paymentiuy')
                datas={'sub_total':sub_total,'discount_price':discount_price,'name':name, 'mob':mob, 'address':address, 'discount':discount, 'user':user.id, 'payment_method':payment_method}
                serialized_data = json.dumps(datas)
                print(serialized_data)
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
                    print('Error creating Razorpay order:', str(e))
                    return JsonResponse({'error': 'Internal Server Error'}, status=500)
                
            else:
                print('bioul;nlkj')
                order=Order.objects.create(user=user,name=name, mob=mob, address=address, total_amount=discount_price, subtotal=sub_total,payment_method=payment_method)
                if discount:
                    order.coupon_discount=discount
                    order.save()
                for item in cart_items:
                    product=Product.objects.get(uid=item.product.uid)
                    product_image=product.product_images.first()
                    product_image_file = File(product_image.image.file)
                    Ordered_item.objects.create(order_id=order,ordered_product_name=product.product_name,unit_price=product.price, qty=item.qty, image=product_image_file)
                cart_items.delete()
                cart.save()
                Payment.objects.create(order=order, payment_method=Payment.PaymentMethod.COD, is_paid=False, amount=discount_price)
                
                print('working')
                return JsonResponse({'url':'/products/order_success/'+str(order.uid)})
        
        context={'cart_items':cart_items,'cart':cart,'len':len, 'addresses':Address.objects.filter(user=user).order_by('-created_at'),'all_coupons':Coupon.objects.filter(is_expired=False)}
    return render(request, 'products/buynow.html', context)

@csrf_exempt
def paymenthandler(request, amount):
    print("Payment Handler endpoint reached")
    print("Content Type:", request.content_type)
    print("Request Parameters:", request.POST)

    serialized_data = cache.get('data')
    print(serialized_data,request.user)
 
    # only accept POST request.
    if request.method == "POST":
        try:
            print('yugilh;', amount)
           
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

                            product=Product.objects.get(uid=product_uid)
                            product_image=product.product_images.first()
                            product_image_file = File(product_image.image.file)

                            order_user=User.objects.get(id=user)
                            order=Order.objects.create(user=order_user,name=name, mob=mob, address=address, total_amount=discount_price, subtotal=sub_total, payment_method=payment_method)
                            if discount:
                                order.coupon_discount=discount
                                order.save()
                            Ordered_item.objects.create(order_id=order,ordered_product_name=product.product_name, unit_price=unit_price,qty=quantity, image=product_image_file)
                
                            print(sub_total, address)
                        else:
                            print('cart')
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
                                product=Product.objects.get(uid=item.product.uid)
                                product_image=product.product_images.first()
                                product_image_file = File(product_image.image.file)
                                Ordered_item.objects.create(order_id=order,ordered_product_name=product.product_name,unit_price=product.price, qty=item.qty, image=product_image_file)
                            cart_items.delete()
                            cart.save()
                
                            print('working')

                    Payment.objects.create(order=order, payment_method=Payment.PaymentMethod.PAYMENT, is_paid=True, razorpay_order_id=razorpay_order_id, rarzorpay_payment_id=payment_id, razorpay_payment_signature=signature, amount=discount_price)
                    razorpay_client.payment.capture(payment_id, amount)
                    print('payment captured',order.uid)
 
                    return redirect('products:order_success',order.uid)
                except:
                    print('failed')

                    return render(request, 'paymentfail.html')
            else:
                print('fail')
                return render(request, 'paymentfail.html')
        except:

            return HttpResponseBadRequest()
    else:
        return redirect('account:login')




@login_required(login_url='account:login')
def order_success(request, uid):
    order=Order.objects.get(uid=uid)
    context={'order':order}
    return render(request, 'products/order_success.html', context)

def shop_page(request):
    context={'products':Product.objects.filter(is_listed=True).order_by('price'), 'categories':Category.objects.all()}
    if request.method=='POST':
        data=json.loads(request.body)
        categories=data['categories']
        sortbyprice=data['sortbyprice']
        print(categories)
        if categories:
            new = []
            for category in categories:
                cat=Category.objects.get(category_name=category)
                products=Product.objects.filter(Category=cat).order_by('price')
                print(cat)
                for product in products:
                    image = ProductImage.objects.filter(product=product).first()

                    product_info = {
                        'name': product.product_name,
                        'price': product.price,
                        'image':image.image.url
                    }
                    new.append({'product': product_info,})
            print(products, new)
            if sortbyprice=='1':
                new_sorted = sorted(new, key=lambda x: x['product']['price'])
            else:
                new_sorted = sorted(new, key=lambda x: x['product']['price'], reverse=True)
            data={'products':new_sorted}
            return JsonResponse(data)
        else:
            if sortbyprice=='1':
                products=Product.objects.filter(is_listed=True).order_by('price')
            else:
                products=Product.objects.filter(is_listed=True).order_by('-price')
            new=[]
            for product in products:
                image = ProductImage.objects.filter(product=product).first()

                product_info = {
                    'name': product.product_name,
                    'price': product.price,
                    'image':image.image.url
                }
                new.append({'product': product_info})
            data={'products':new}
            return JsonResponse(data)
    return render(request, 'shop.html', context)


def apply_coupon(request):
    if request.method=='POST':
        data=json.loads(request.body)
        coupon_uid=data['coupon_uid']
        total=data['total']
        coupon=Coupon.objects.get(uid=coupon_uid,)
        if coupon.is_expired==True:
            data = {'fail':'Coupon Expired'}
            return JsonResponse(data)
        elif int(total)>=coupon.minimum_amount:
            discount=int(total)-coupon.discount_price
            data={'success':'coupon applied', 'discount':discount}
            return JsonResponse(data)
        else:
            data = {'fail': f'Coupon is valid for orders greater than {coupon.minimum_amount} rupees  '}
        return JsonResponse(data)