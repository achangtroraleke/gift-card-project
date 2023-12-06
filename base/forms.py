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