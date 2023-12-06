from django import forms
from django.forms import ModelForm
from .models import Card, Customer

class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = '__all__'

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class PurchaseForm(forms.Form):
    total = forms.FloatField(label="Total Amount")