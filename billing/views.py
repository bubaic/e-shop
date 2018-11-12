from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from fup.stripe_info import STRIPE_PK, stripe

from billing.models import BillingProfile, Card

# Create your views here.
def payment_method(request):
    billing_profile, created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect('/cart')

    next_url = None
    next_get = request.GET.get('next')

    if is_safe_url(next_get, request.get_host()):
        next_url = next_get
    return render(request, 'billing/payments.html', {
        'publish_key': STRIPE_PK,
        'next_url': next_url
    })

def payment_create(request):
    if request.method == 'POST' and request.is_ajax():
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({'message': 'User doesn\'t exist.'}, status=401)

        token = request.POST.get('token')
        if token is not None:
            new_card  = Card.objects.add_new(billing_profile, token)
        return JsonResponse({'message': 'Success! Your card has been added successfully.'})
    return HttpResponse('Error!', status=400)