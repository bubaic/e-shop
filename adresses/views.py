from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import AddressForm
from billing.models import BillingProfile
from .models import Address

# Create your views here.
def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        'form': form,
    }
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None

    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + '_address_id'] = instance.id
            print()
        else:
            print("Some error occurred here!")
            return redirect('cart:checkout')

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect('cart:checkout')

def address_use_view(request):
    if request.user.is_authenticated:
        context = {}
        next_get = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_get or next_post or None

        if request.method == 'POST':
            address_type = request.POST.get('address_type', 'shipping')
            shipping_address = request.POST.get('shipping_address', None)
            billing_profile, created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + '_address_id'] = shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect('cart:checkout')