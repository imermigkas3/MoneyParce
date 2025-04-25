from django.forms import ModelForm
from .models import Transaction
from django import forms

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'category']

class EmailForm(forms.Form):
    email_address = forms.EmailField(label="", widget=forms.TextInput(attrs={
            "class": "rounded   p-1 w-100 border",
            "placeholder": "Enter email here...",
            "autocomplete": "off",
        }))