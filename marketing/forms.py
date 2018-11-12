from django import forms
from .models import MarketingPreference

class MktPrefForm(forms.ModelForm):
    subscribed = forms.BooleanField(required=False)
    class Meta:
        model = MarketingPreference
        fields = ['subscribed',]