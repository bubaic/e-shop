from django.contrib import admin
from .models import MarketingPreference

# extended models
class MktPrefAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'mc_subscribed', 'updated']
    list_filter = ['subscribed', 'updated']
    readonly_fields = [
        'mailchimp_msg',
        'mc_subscribed',
        'timestamp',
        'updated'
    ]
    class Meta:
        model = MarketingPreference
        fields = [
            'user',
            'subscribed',
            'mailchimp_msg',
            'mc_subscribed',
            'timestamp',
            'updated'
        ]

# Register your models here.
admin.site.register(MarketingPreference, MktPrefAdmin)