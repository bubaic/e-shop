from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """
        A form for creating new users. Includes all the required
        fields, plus a repeated password.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super().__init__(*args, **kwargs)

    password1   = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2   = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """
        A form for updating users. Includes all the fields on the user,
        but replaces the password field with admin's password hash
        display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class GuestForm(forms.Form):
    email = forms.EmailField(label_suffix='', widget=forms.EmailInput())

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email Address'}
        ))
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '••••••••'}
        )
    )

class RegisterForm(forms.ModelForm):
    """
        A form for registering new users. Includes all
        the required fields, plus a repeated password.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super().__init__(*args, **kwargs)

    email = forms.EmailField(label='Email Address',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Email Address'}
                             ))
    first_name  = forms.CharField(label='Firstname',
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Firstname'}
                                  ))
    last_name   = forms.CharField(label='Lastname',
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Lastname'}
                                  ))
    password1   = forms.CharField(label='Password',
                                  widget=forms.PasswordInput(
                                      attrs={'class': 'form-control', 'placeholder': '••••••••'}
                                  ))
    password2   = forms.CharField(label='Confirm Password',
                                  widget=forms.PasswordInput(
                                      attrs={'class': 'form-control', 'placeholder': '••••••••'}
                                  ))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active = False
        if commit:
            user.save()
        return user


# class RegisterForm(forms.Form):
#     first_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Fullname'
#             }
#         ),
#         label=''
#     )
#     last_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Username'
#             }
#         ),
#         label=''
#     )
#     email = forms.EmailField(
#         widget=forms.EmailInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Email'
#             }
#         ),
#         label=''
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': '••••••••'
#             }
#         ),
#         label=''
#     )
#     password2 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': '* * * *'
#             }
#         ),
#         label=''
#     )
#
#     def clean(self):
#         data = self.cleaned_data
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#         password2 = self.cleaned_data.get('password2')
#         email = self.cleaned_data.get('email')
#
#         qs = User.objects.filter(username=username)
#         if qs.exists():
#             raise forms.ValidationError(username +" is already taken")
#
#         qs2 = User.objects.filter(email=email)
#         if qs2.exists():
#             raise forms.ValidationError(email + " is already taken")
#
#         if password2 != password:
#             raise forms.ValidationError("Passwords doesn't match!")
#         return data