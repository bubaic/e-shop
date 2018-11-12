from django.conf.urls import url

from .views import checkout_address_create_view, address_use_view

app_name = 'adresses'

urlpatterns = [
    url(r'^$', checkout_address_create_view, name='address_view'),
    url(r'reuse/$', address_use_view, name='address_use')
]