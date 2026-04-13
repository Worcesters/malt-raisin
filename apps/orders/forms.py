from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(label="Prénom", max_length=100)
    last_name = forms.CharField(label="Nom", max_length=100)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Téléphone", max_length=20, required=False)
    address = forms.CharField(label="Adresse", widget=forms.Textarea(attrs={"rows": 3}))
    city = forms.CharField(label="Ville", max_length=100)
    postal_code = forms.CharField(label="Code postal", max_length=10)
