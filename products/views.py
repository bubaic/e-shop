from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product
from cart.models import Cart
from analytics.mixin import ObjectViewedMixin

# Create your views here.

class ProductFeaturedListView(ListView):
    template_name = 'products/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    template_name = 'products/featured-detail.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/list.html'

    # catch the context object by a method without `context_object_name`
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    #     another way to obtain data
    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)

"""
function based view for Product Lists
"""
# def product_list_view(request):
#     qs = Product.objects.all()
#     ctx = {
#         'object_list': qs
#     }
#     return render(request, 'products/list.html', ctx)

class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = 'products/details.html'
    context_object_name = 'prod'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Product doesn't exist")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        return instance

class ProductDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = 'products/details.html'
    context_object_name = 'prod'

    # catch the context object by a method without `context_object_name`
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Oops...! Product not found.")
        return instance

    #     another way to obtain data
    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)

"""
function based view for Product Details
"""
# def product_detail_view(request, pk=None, *args, **kwargs):
    # qs = Product.objects.get(pk=pk)
    # instance = get_object_or_404(Product, pk=pk)
    # '''
    # basic lookup from database
    # '''
    # try:
    #     instance = Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     raise Http404('Product not found!')
    # except:
    #     print('Huh?')
    #
    # shortcut-method:
    # instance = Product.objects.get_by_id(pk)
    # if instance is None:
    #       raise Http404('Product not found')
    #
    #  or, other ways as below ...
    #
    # qs = Product.objects.get(pk=pk)
    # if qs.exists() and (qs.count() > 0):
    #     instance = qs.first()
    # else:
    #     raise Http404('Product not found!')
    #
    # ctx = {
    #     'object': instance
    # }
    # return render(request, 'products/details.html', ctx)