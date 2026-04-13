from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Votre nom", max_length=200)
    email = forms.EmailField(label="Votre email")
    subject = forms.CharField(label="Sujet", max_length=300)
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={"rows": 5}))
