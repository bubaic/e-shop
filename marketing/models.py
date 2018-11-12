from django.contrib import admin
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from .utils import Mailchimp

mc_obj = Mailchimp()

# Create your models here.
class MarketingPreference(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed      = models.BooleanField(default=True)
    mc_subscribed   = models.NullBooleanField(blank=True)
    mailchimp_msg   = models.TextField(null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


def mkt_pref_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        MarketingPreference.objects.get_or_create(user=instance)

post_save.connect(mkt_pref_create_receiver, sender=settings.AUTH_USER_MODEL)

def mkt_pref_update_receiver(sender, instance, created, *args, **kwargs):
    if created:
        status_code, response_data = mc_obj.subscribe(instance.user.email)

post_save.connect(mkt_pref_update_receiver, sender=MarketingPreference)

def mkt_subs_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mc_subscribed:
        if instance.subscribed:
            print(instance.user.email)
            status_code, response_data = mc_obj.subscribe(instance.user.email)
        else:
            status_code, response_data = mc_obj.unsubscribe(instance.user.email)

        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mc_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mc_subscribed = False
            instance.mailchimp_msg = response_data

pre_save.connect(mkt_subs_receiver, sender=MarketingPreference)
