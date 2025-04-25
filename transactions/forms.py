from django.forms import ModelForm
from .models import Transaction
from django import forms

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'category']

class EmailForm(forms.Form):
    recipient_email = forms.CharField()