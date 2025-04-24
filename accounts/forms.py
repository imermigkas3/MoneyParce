from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from .models import Income, UserProfile

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self
        ]))

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user already with this email exists. Please use a different email address.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists. Please choose a different username.")
        return username

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("There is no user account that exists with this email address. Please provide a valid email address that is registered with MoneyParce or go back to login and create a new account.")
        return email

class IncomeForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,  # Ensure it's a positive number
        error_messages={'min_value': 'Please enter a positive income amount.'}
    )

    class Meta:
        model = Income
        fields = ['amount']

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=150,
        validators=[UnicodeUsernameValidator()])
    email = forms.EmailField(required=True, label='Email Address')

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'status', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance and self.instance.user and self.instance.user.username == username:
            return username  # No change, so it's valid

        if User.objects.filter(username=username).exists():
            raise ValidationError("This username address is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance and self.instance.user and self.instance.user.email == email:
            return email  # No change, so it's valid

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if self.has_changed():
            if 'email' in self.changed_data:
                user_profile.user.email = self.cleaned_data['email']
            if 'username' in self.changed_data:
                user_profile.user.username = self.cleaned_data['username']
            user_profile.user.save()
        if commit:
            user_profile.save()
        return user_profile