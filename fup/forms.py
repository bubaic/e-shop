from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }
        )
    )
    msg = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Type some message here'
            }
        )
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        # patterns = ['co.in', 'co.uk', 'co.au', 'co.il']
        if not ('gmail.com' or 'yahoo.com' or 'ymail.co.*' or 'outlook.' or 'hotmail.com') in email:
            raise forms.ValidationError("Hmm... it doesn't look like a valid email!")
        return email