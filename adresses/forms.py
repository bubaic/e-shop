from django import forms
from .models import Address
from fup.local_vars import DEFAULT_COUNTRIES_LIST

class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(AddressForm, self).__init__(*args, **kwargs)

    address_line_1 = forms.CharField(
        label="Address Line 1",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Address Line 1'
            }
        )
    )
    address_line_2 = forms.CharField(
        label="Address Line 2",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Address Line 2 (optional)'
            }
        ),
    )
    city = forms.CharField(
        label= "City",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }
        ),
    )
    zipcode = forms.CharField(
        label= "Zipcode",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Zipcode'
            }
        ),
    )
    state = forms.CharField(
        label="State",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }
        ),
    )
    country = forms.ChoiceField(
        label="Country",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': ''
            }
        ),
        choices=DEFAULT_COUNTRIES_LIST,
    )

    class Meta:
        model = Address
        fields = (
            'address_line_1',
            'address_line_2',
            'city',
            'zipcode',
            'state',
            'country'
        )