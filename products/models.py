import os, random
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse

from fup.utils import unique_slug_generator

# Create your models here.

def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def get_image_path(instance, file):
    new_file = random.randint(1, 4560879120)
    name, ext = get_file_ext(file)
    final_ = f'{new_file}{ext}'      # f-string for formatting
    return f'products/{new_file}/{final_}'

# custom queryset
class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True, active=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookup = Q(title__icontains=query) |\
                 Q(description__icontains=query) |\
                 Q(price__icontains=query) |\
                 Q(tag__title__icontains=query)
        return self.filter(lookup).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def is_featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() > 0:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    image = models.FileField(upload_to=get_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def get_absolute_url(self):
        # return f'/products/{self.slug}/'
        return reverse('products:detail', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

def product_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_reciever, sender=Product)