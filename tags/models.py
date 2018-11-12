from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from products.models import Product
from fup.utils import unique_slug_generator

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title

def tag_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_reciever, sender=Tag)