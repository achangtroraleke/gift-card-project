from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Card, Customer, Transaction, MyCustomUser, Business
from django.contrib.auth.forms import UserCreationForm

class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
        exclude = ('original_balance', 'business', 'card_num', 'is_active')

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['created_by']

class TransactionForm(forms.Form):
    total = forms.FloatField(label="Total Amount")
    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get("total")
   
        if total < 0 or total < .01:
            raise ValidationError(
                "Cannot make a purchase with value less than $0.00."
            )
        
class MyUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = MyCustomUser
        fields = ['username',  'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model= MyCustomUser
        fields = ['email', 'password']

class EditUserForm(ModelForm):
    
    class Meta:
        model = MyCustomUser
        fields = ['email', 'first_name', 'last_name']


class NewBusinessForm(ModelForm):
    business_image = forms.ImageField()
    class Meta:
        model = Business
        fields = ['name']