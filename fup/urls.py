from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

from .views import home, contact_page, about_page
from accounts.views import RegisterView, LoginView, guest_register_view
from cart.views import cart_detail_api_view

urlpatterns = [
    # home view
    url(r'^$', home, name='home'),
    # api view
    url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
    # contact views
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^about/$', about_page, name='about'),
    # account views
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^accounts/$', RedirectView.as_view(url='/account')),
    url(r'^account/', include('accounts.urls', namespace='accounts')),
    url(r'^accounts/', include('accounts.passwords.urls')),
    url(r'^register/guest/$', guest_register_view, name='guest_register'),
    # module views
    url(r'', include('products.urls', namespace='products')),
    url(r'', include('marketing.urls', namespace='marketing')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^billing/', include('billing.urls', namespace='billing')),
    url(r'^checkout/address/', include('adresses.urls', namespace='adresses')),
    # admin view
    url(r'^admin/', admin.site.urls, name='admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
