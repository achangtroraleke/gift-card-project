from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Card, Customer, Transaction

class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
        exclude = ('original_balance',)

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class TransactionForm(forms.Form):
    total = forms.FloatField(label="Total Amount")
    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get("total")
   
        if total < 0 or total < .01:
            raise ValidationError(
                "Cannot make a purchase with value less than $0.00."
            )