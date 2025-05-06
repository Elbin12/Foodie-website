from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from . models import *
from products.models import *
from django.contrib import messages
from .utils import generate_otp, send_otp_email, get_otp_from_session
from django.views.decorators.cache import cache_control
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json
import razorpay
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden



from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.template.loader import get_template



from django.core.files.base import ContentFile

import jinja2
import pdfkit


from decouple import config
# Create your views here.


def signup(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        gender=request.POST.get('selectedGender')
        email=request.POST.get('email')
        mob=request.POST.get('mobile')
        password=request.POST.get('password')
        confirm=request.POST.get('confirm_password')

        request.session['first_name']=first_name
        request.session['last_name'] = last_name
        request.session['gender'] = gender
        request.session['email'] = email
        request.session['password'] = confirm
        request.session['mob'] = mob
        
        user=User.objects.filter(email=email)
        if user.exists():
            messages.warning(request, 'Email is already taken. Use another one.')
            return redirect('account:signup')
        else:
            otp = generate_otp()
            request.session['otp'] = otp
            send_otp_email(email, otp)
            return render(request,'account/otp.html',{"email":email})
    return render(request, 'account/signup.html')

def resend(request):
    if request.method=='POST':
        email=json.loads(request.body)['email']
        otp = generate_otp()
        request.session['otp'] = otp
        send_otp_email(email, otp)
        data={'success':'Another OTP is sent to your email'}
        return JsonResponse(data)



def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = get_otp_from_session(request)

        if stored_otp and stored_otp == entered_otp:
            hashed_password=make_password(request.session['password'])
            user=User.objects.create(username=request.session['email'], first_name=request.session['first_name'], last_name=request.session['last_name'],password=hashed_password, email=request.session['email'])
            profile=Profile.objects.create(user=user , gender=request.session['gender'] ,mobile_number=request.session['mob']) 
            Cart.objects.create(user=user) 
            Wallet.objects.create(user=user)          
            request.session['username'] = user.username
            request.session['email'] = None
            request.session['password'] = None
            request.session['mob'] = None
            messages.success(request, 'Sign up is done successfullly. Please login')
            return redirect('account:login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('account:otp_verification')
    return render(request, 'account/otp.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_page(request):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user=request.user)
        if profile.block:
            messages.warning(request,'You are blocked')
            return redirect('account:login')
        else:
            return redirect('home:home')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        user=authenticate(username=email, password=password)

        if user:
            profile=Profile.objects.get(user=user)
            if profile.block:
                messages.warning(request,'You are blocked')
                return redirect('account:login')
            else:
                login(request,user)
                request.session['username']=email
                return redirect('home:home')
        else:
            messages.error(request, 'Enter valid username and password')
            return redirect('account:login')          
    return render(request, 'account/login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def app_logout(request):
    if 'username' in request.session:
        logout(request)
    return redirect('account:login')

def forgot_password(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        otp=request.POST.get('OTP')
        user=User.objects.get(email=email)
        if otp==request.session['otp']:
            hashed_password=make_password(password)
            user.password=hashed_password
            user.save()
            messages.success(request,'Password reset done. Login with this password.')
            return redirect('account:login')
        else:
            messages.warning(request,"OTP doesn't match")
            return redirect('account:forgot_password')
    return render(request, 'account/forgot_password.html')

def verify(request):
    if request.method=='POST':
        Data=json.loads(request.body)
        email=Data['email']
        user = User.objects.filter(email=email).first()
        if User.objects.filter(email=email).exists() and Profile.objects.filter(user=user).exists():
            otp = generate_otp()
            request.session['otp'] = otp
            send_otp_email(email, otp)
            data={'success':'An OTP is sent to your email'}
            return JsonResponse(data)
        else:
            data={'fail':'Account not found'}
            return JsonResponse(data)    
        
@login_required(login_url='account:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_to_cart(request):
    if request.method=='POST':
        data=json.loads(request.body)
        uid=data['uid']
        selected=data['selected_values']
        print(selected, 'selectedddd')
        values=[]
        for value in selected:
            val=Attribute_values.objects.get(value=value)
            values.append(val)
        product=Product.objects.get(uid=uid)
        print(values, 'values')
        try:
            product_attribute=ProductAttribute.objects.filter(product=product)
            for value in values:
                print(value, 'oldkd')
                product_attribute = product_attribute.filter(value=value)
            print(product_attribute.first(), 'ikdd')
            product_attribute = product_attribute.first()
            cart=Cart.objects.get(user=request.user)
            if Cart_item.objects.filter(cart=cart,product_attribute=product_attribute).exists():
                data={'exists':'Food item is already in your cart'}
                return JsonResponse(data)
            else:
                new=Cart_item.objects.create(cart=cart, product=product, product_attribute=product_attribute)
                new.is_added=True
                new.save()
                cart.save()
                data={'success':'Food item is added to your cart'}
                return JsonResponse(data)
        except Cart.DoesNotExist:
            data={'fail':'Please log in to visit your cart'}
            return JsonResponse(data)
        except Exception as e:
            print(e, 'dkfgkfg')
            data={'fail':'Item not in stock'}
            return JsonResponse(data)
    
@login_required(login_url='account:login')
def cart(request):
    try:
        cart=Cart.objects.get(user=request.user)
        cart_items = cart.cart_items.select_related('product').order_by('product__product_name')
        print(cart_items, 'cart items')
        products = [
            {'product': item.product,'val':item.product_attribute, 'qty': item.qty, 'price':item.price, 'is_available':item.product.is_listed}
            for item in cart_items
        ]
        print(products)
        for i in products:
            count=products.__len__()
        if not products:
            context={'warning':'Your cart is empty'}
            return render(request, 'account/cart.html',context)
        else:
            context={'products':products, 'count':count,'price':cart.total}
    except:
        context={'warning':'you must login to visit the cart'}
        return render(request, 'account/cart.html',context)
    return render(request, 'account/cart.html',context)

def change(request):
    if request.method=='POST':
        data = json.loads(request.body)

        if 'qty' in data:
            qty=data['qty']
            uid=data['uid']
            
            product=ProductAttribute.objects.get(uid=uid)
            cart=Cart.objects.get(user=request.user)
            cart_item=Cart_item.objects.get(cart=cart,product_attribute=product)
            cart_item.qty=qty
            cart_item.save()
            cart.save()

            if 'coupon' in data:
                coupon_uid = data['coupon']
                coupon = Coupon.objects.get(uid=coupon_uid)
                if cart.total < coupon.minimum_amount:
                    data={'qty':cart_item.qty,'price':cart_item.price,'total':cart.total,'coupon_fail':'Coupon removed'}
                    return JsonResponse(data)
                else:
                    data={'qty':cart_item.qty,'price':cart_item.price,'total':cart.total}
                    return JsonResponse(data)
            else:
                data={'qty':cart_item.qty,'price':cart_item.price,'total':cart.total}
                return JsonResponse(data)
        else:
            uid=data['uid']
            total = data['totalPrice']
            product=ProductAttribute.objects.get(uid=uid)
            if 'coupon' in data:
                coupon_uid = data['coupon']
                coupon = Coupon.objects.get(uid=coupon_uid)
                if total < coupon.minimum_amount:
                    data={'coupon_fail':'Coupon removed','total':total}
                    return JsonResponse(data)
                else:
                    data={'success':'success', 'total':total}
                    return JsonResponse(data)
            else:
                data={'success':'success','total':total}
        return JsonResponse(data)

def delete(request):
    if request.method=='POST':
        uid=json.loads(request.body)['uid']
        product=ProductAttribute.objects.get(uid=uid)
        cart=Cart.objects.get(user=request.user)
        cart_item=Cart_item.objects.filter(product_attribute=product)
        cart_item.delete()
        cart.save()
        l=cart.cart_items.all()
        len=l.__len__()
        data={'success':'true','len':len,'price':cart.total}
    return JsonResponse(data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='account:login')
def account(request):
    try:
        profile=Profile.objects.get(user=request.user)
        context={'profile':profile}
    except:
        return redirect('home:home')
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        gender=request.POST.get('selectedGender')
        user=User.objects.get(username=request.user.username)
        # profile=Profile.objects.get(user=user)
        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        profile.gender=gender
        profile.mobile_number=mobile
        user.save()
        profile.save()

        return redirect('account:account')
    return render(request, 'account/account.html',context)

@login_required(login_url='account:login')
def check_otp(request):
    if request.method=='POST':
        otp=json.loads(request.body)['otp']
        if otp==request.session['otp']:
            data={'success':'Your email successfully verified. Now you can edit your email to a new one.'}
        else:
            data={'fail':'Wrong otp'}
        return JsonResponse(data)

@login_required(login_url='account:login')
def manage_addresses(request):
    addresses=Address.objects.filter(user=request.user).order_by('name')
    context={'addresses':addresses}
    if request.method=='POST':
        name=request.POST.get('name')
        mobile=request.POST.get('mobile')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        locality=request.POST.get('locality')
        city=request.POST.get('city')
        state=request.POST.get('state')
        
        user=User.objects.get(username=request.user)
        address=Address.objects.create(user=user, name=name,mobile_number=mobile,pincode=pincode,address=address,city=city,state=state,locality=locality)
        address.save()
        
        return redirect('account:addresses')
    return render(request, 'account/manage_addresses.html',context)

@login_required(login_url='account:login')
def edit_address(request,uid):
    if request.method=='POST':
        address_instance=Address.objects.get(uid=uid)
        if request.user.id != address_instance.user.id:
            messages.error(request, "You are not authorized to edit this address.",extra_tags='auth')
            return redirect('account:addresses')
        name=request.POST.get('name')
        mobile=request.POST.get('mobile')
        pincode=request.POST.get('pincode')
        locality=request.POST.get('locality')
        shipping_address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')

        address_instance.name=name 
        address_instance.mobile_number=mobile
        address_instance.pincode=pincode
        address_instance.locality=locality
        address_instance.address=shipping_address
        address_instance.city=city
        address_instance.state=state    
        address_instance.save()
        
        return redirect('account:addresses')

@login_required(login_url='account:login')   
def edit_address_from_checkout(request):
    if request.method=='POST':
        data=json.loads(request.body)
        name=data['name']
        mobile=data['mobile']
        pincode=data['pincode']
        locality=data['locality']
        shipping_address=data['shipping_address']
        city=data['city']
        state=data['state']
        uid=data['uid']


        address_instance=Address.objects.get(uid=uid)
        address_instance.name=name 
        address_instance.mobile_number=mobile 
        address_instance.pincode=pincode
        address_instance.locality=locality
        address_instance.address=shipping_address
        address_instance.city=city
        address_instance.state=state    
        address_instance.save()

        data={'success': 'Address edited successfully'}
        return JsonResponse(data)

@login_required(login_url='account:login')
def add_address_from_checkout(request):
    if request.method=='POST':
        data=json.loads(request.body)
        name=data['name']
        mobile=data['mobile']
        pincode=data['pincode']
        locality=data['locality']
        shipping_address=data['shipping_address']
        city=data['city']
        state=data['state']

        user=User.objects.get(username=request.user)
        address=Address.objects.create(user=user, name=name,mobile_number=mobile,pincode=pincode,address=shipping_address,city=city,state=state,locality=locality)

        data={'success': 'Address added successfully'}
        return JsonResponse(data)

@login_required(login_url='account:login')
def delete_address(request):
    uid=json.loads(request.body)['uid']
    if request.method=='POST':
        address=Address.objects.get(uid=uid)
        address.delete()
        data={'success':'true'}
    return JsonResponse(data)

@login_required(login_url='account:login')
def my_orders(request):
    orders=Order.objects.filter(user=request.user).order_by('-created_at')
    ordered_items=[]
    for order in orders:
        ordered_item = Ordered_item.objects.filter(order_id=order)
        ordered_items.append(ordered_item)
    context={'orders':orders,'ordered_items':ordered_items}
    return render(request, 'account/my_orders.html', context)

@login_required(login_url='account:login')
def order_details(request, uid):
    try:
        order=Order.objects.get(uid=uid)
        if request.user.id != order.user.id:
            messages.error(request, "You are not authorized to view this order.",extra_tags='auth')
            return redirect('account:my_orders')
    except Exception as e:
        print(e)
    ordered_items=Ordered_item.objects.filter(order_id=order)
    context={'order':order, 'ordered_items':ordered_items}
    return render(request, 'account/order_details.html', context)

@login_required(login_url='account:login')
def cancel_request(request, uid):
    order=Order.objects.get(uid=uid)
    order.cancel_request=True
    order.save()
    return redirect('account:order_details',uid)




@login_required(login_url='account:login')
def coupons(request):
    coupons = Coupon.objects.filter(is_expired=False)
    applied_coupons=Coupon.objects.filter(is_expired=True)
    context={'coupons':coupons, 'applied_coupons':applied_coupons}
    return render(request, 'account/coupons.html',context)


razorpay_client=razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required(login_url='account:login')
def wallet(request):
    wallet=Wallet.objects.get(user=request.user)
    order=Order.objects.filter(user=request.user)
    payments=[payment for payment in Payment.objects.filter(payment_method=Payment.PaymentMethod.PAYMENT, order__uid__in=[i.uid for i in order])]
    transactions=Transaction.objects.filter(wallet=wallet).all()
    context={ 'wallet':wallet,'transactions':transactions }
    if request.method=='POST':
        currency = 'INR'
        amt=json.loads(request.body)['amount']
        amount = int(amt) * 100  

        user=User.objects.get(username=request.user)
        datas={'user':user.id}
        serialized_data = json.dumps(datas)
        cache.set('data',serialized_data)
        try:
            razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
            razorpay_order_id = razorpay_order['id']
            callback_url = config('CALLBACK_URL') + '/account/paymenthandler/'+str(amount/100)

            context = {
                'amount': amount,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_merchant_key': settings.RAZOR_KEY_ID,
                'razorpay_amount': amount,
                'currency': currency,
                'callback_url': callback_url,
            }

            return JsonResponse(context)
        except Exception as e:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    return render(request, 'account/wallet.html', context)

@csrf_exempt
def paymenthandler(request, amount):
    serialized_data = cache.get('data')
    if request.method == "POST":
        # get the required parameters from post request.
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            data = json.loads(serialized_data)
            user=data['user']
    
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                try:
                    amount = int(Decimal(amount) * 100)
                    razorpay_client.payment.capture(payment_id, amount)
                    wallet=Wallet.objects.get(user=user)
                    wallet.balance+=amount/100
                    Transaction.objects.create(wallet=wallet, amount=amount/100, transaction_type=Transaction.Type.DEPOSIT)
                    wallet.save()
                    return redirect('account:wallet')
                except:
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
        except:
            return redirect('account:wallet')
            
    else:
        # if signature verification fails.
        return render(request, 'paymentfail.html')


@login_required(login_url='account:login')
def wishlist(request):
    wishlist=Wishlist.objects.get_or_create(user = request.user)
    w = Wishlist.objects.get(user=request.user)
    context = {'wishlist':w}
    return render(request, 'account/wishlist.html', context)

@login_required(login_url='account:login')
def add_to_wishlist(request,uid):
    product_attribute=ProductAttribute.objects.get(uid=uid)
    wishlist=get_object_or_404(Wishlist, user=request.user)
    wishlist.products.add(product_attribute)
    wishlist.save()
    return redirect('account:wishlist')

@login_required(login_url='account:login')
def whishlist_delete(request, uid):
    product_attribute=ProductAttribute.objects.get(uid=uid)
    wishlist=get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product_attribute)
    wishlist.save()
    return redirect('account:wishlist')


def invoice(request, uid):
    order=Order.objects.get(uid=uid)
    context={'order':order}
    return render(request, 'pdf.html', context)
    