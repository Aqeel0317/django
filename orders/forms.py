from django import forms
from .models import Order

PAYMENT_METHOD_CHOICES = [
    ('paypal', 'PayPal'),
    ('easypaisa', 'Easypaisa'),
]

class OrderCreateForm(forms.ModelForm):
    country = forms.CharField(max_length=100, required=True)
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'country', 'payment_method']
