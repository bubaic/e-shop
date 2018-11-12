from django.db import models

from billing.models import BillingProfile
from fup.local_vars import ADDRESS_TYPES, DEFAULT_COUNTRIES_LIST

# Create your models here.

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    country = models.CharField(max_length=120, choices=DEFAULT_COUNTRIES_LIST, default='India')

    def __str__(self):
        return str(self.billing_profile)

    def get_addr(self):
        return f"{self.address_line_1} {self.address_line_2}, {self.city}, {self.state} &mdash; {self.zipcode}"