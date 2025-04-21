from django import forms

class ChatForm(forms.Form):
    your_message = forms.CharField(label="")
