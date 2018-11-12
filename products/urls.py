from django.conf.urls import url
from .views import ProductListView, ProductDetailView, ProductFeaturedDetailView,\
                   ProductFeaturedListView, ProductDetailSlugView

app_name = 'products'

urlpatterns = [
    url(r'^products/$', ProductListView.as_view(), name='list'),
    # url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='idetl'),
    url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    # url(r'^featured/$', ProductFeaturedListView.as_view()),
    # url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),
]
