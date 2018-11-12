import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from accounts.forms import LoginForm, GuestForm
from adresses.forms import AddressForm

from .models import Cart
from accounts.models import Guest
from adresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product

from fup.local_vars import DEFAULT_COUNTRIES_LIST
from fup.stripe_info import stripe, STRIPE_PK

# Create your views here.

def create_cart(user=None):
    cart_obj = Cart.objects.create(user=None)
    print('new cart created')
    return cart_obj

def cart_detail_api_view(request):
    # 'image': json.dumps(str(i.image))
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [
        {
            'id': i.id,
            'url': i.get_absolute_url(),
            'name': i.title,
            'description': i.description,
            'price': i.price
        }
        for i in cart_obj.products.all()
    ]
    cart_data = {'products': products, 'subtotal': cart_obj.subtotal, 'total': cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    '''
        # usr = User.objects.get(id=request.user.id)
        # del request.session['cart_id']
        # if cart_id is None:
        #     cart_obj = create_cart(usr)
        #     print("cart obj ID: ", cart_obj.id)
        #     request.session['cart_id'] = cart_obj.id
        # else:
        # cart_id = request.session.get('cart_id', None)
        # qs = Cart.objects.filter(id=cart_id)
        # if qs.count() > 0:
        #     print('cart id exists: ', cart_id)
        #     cart_obj = qs.first()
        #     if request.user.is_authenticated() and cart_obj.user is None:
        #         cart_obj.user = request.user
        #         cart_obj.save()
        # else:
        #     # cart_obj = create_cart(usr)
        #     cart_obj = Cart.objects.new(user=request.user)
        #     request.session['cart_id'] = cart_obj.id
    '''

    cart_obj, new_obj = Cart.objects.new_or_get(request)

    # print("cart objects\n",cart_obj, "\n new objects\n", new_obj)
    # products = cart_obj.products.all()
    # total = 0
    # for x in products:
    #     total += x.price
    # cart_obj.total = total
    # cart_obj.save()
    return render(request, "cart/home.html", {'cart':cart_obj})

def update_cart(request):
    prod_id = request.POST.get('product_id')
    if prod_id is not None:
        try:
            prod_obj = Product.objects.get(id=prod_id)
        except Product.DoesNotExist:
            return redirect('cart:cart')
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if prod_obj in cart_obj.products.all():
            cart_obj.products.remove(prod_obj)
            added = False
        else:
            cart_obj.products.add(prod_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()

        if request.is_ajax():
            json_response = {
                'added': added,
                'removed': not added,
                'cartItemCount': cart_obj.products.count()
            }
            return JsonResponse(json_response)
    return redirect('cart:cart')

def checkout_home(request):
    cart_obj, new_cart = Cart.objects.new_or_get(request)
    order_obj = None

    if new_cart or cart_obj.products.count() == 0:
        return redirect('cart:cart')

    # user = request.user
    # billing_profile = None

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    # guest_email_id = request.session.get('guest_id')
    #
    # if user.is_authenticated:
    #     # if user.email:
    #     billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
    #                                                     user=user, email=user.email)
    # elif guest_email_id is not None:
    #     guest_email_obj = Guest.objects.get(id=guest_email_id)
    #     billing_profile, billing_guest_created = BillingProfile.objects.get_or_create(
    #                                                 email=guest_email_obj.email)
    # else:
    #     pass

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_created = Order.objects.new_or_get(billing_profile, cart_obj)

        # order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        # if order_qs.count() > 0:
        #     order_obj = order_qs.first()
        # else:
        #     old_order = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
        #     if old_order.exists():
        #         old_order.update(active=False)
        #     order_obj = Order.objects.create(cart=cart_obj,
        #                  billing_profile = billing_profile)

        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == 'POST':
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_card_inactive()
                return redirect('cart:success')
            else:
                print(crg_msg)
                return redirect('cart:checkout')

    countries = DEFAULT_COUNTRIES_LIST

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'billing_address_form': billing_address_form,
        'country': countries,
        'address_qs': address_qs,
        'has_card': has_card,
        'publish_key': STRIPE_PK
    }
    return render(request, 'cart/checkout.html', context)

def checkout_done(request):
    return render(request, 'cart/checkout-done.html', {})