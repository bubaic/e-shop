from django.conf.urls import url
from .views import cart_home, update_cart, checkout_home, checkout_done

app_name = 'cart'

urlpatterns = [
    url(r'^$', cart_home, name='cart'),
    url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^update/$', update_cart, name='update'),
    url(r'^success/$', checkout_done, name='success')
]
