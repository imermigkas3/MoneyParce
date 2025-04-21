from django import forms

class ChatForm(forms.Form):
    your_message = forms.CharField(label="", widget=forms.TextInput(attrs={
            "class": "rounded-pill   p-1 w-100 border",
            "placeholder": "   Type your message..."
        }))