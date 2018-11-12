from django.conf.urls import url
from .views import payment_method, payment_create

app_name = 'billing'

urlpatterns = [
    url(r'^payment/$', payment_method, name='bill-pay'),
    url(r'^payment/create/$', payment_create, name='pay-create'),
]