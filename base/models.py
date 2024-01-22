from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.mail import send_mail

# Create your models here.

class MyCustomUser(AbstractUser):
    name = models.CharField(max_length=200, null=True, )    
    email = models.EmailField(max_length=100, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Customer(models.Model):
    first_name = models.CharField(max_length=25, null=True, blank=True, unique=False)
    last_name = models.CharField(max_length=25, null=True, blank=True, unique=False)
    created_by = models.ForeignKey(MyCustomUser, related_name='customers', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f'{self.first_name.title()} {self.last_name.title()} '
    
class Business(models.Model):
    name = models.CharField(max_length=200, unique=False, null=False)
    owner = models.ForeignKey(MyCustomUser, related_name='businesses', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    gc_total_bal = models.FloatField(default=0, validators=[MinValueValidator(0)])
    bus_img = models.ImageField(null=True, default='storefront.svg')
    
    def __str__(self):
        return f'{self.name}'
    
    def update_balance(self, amount):
        self.gc_total_bal += amount
       
    
class Card(models.Model):
    card_num = models.IntegerField(default=0, null=True)
    original_balance = models.FloatField(default=0)
    balance = models.FloatField(default=0, validators=[MinValueValidator(0)])
    updated = models.DateTimeField(auto_now=True)   
    created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, related_name='gift_cards', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    business = models.ForeignKey(Business, related_name='gift_cards', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Card #{self.id}'
    
    def affordable(self, purchase_amount):
        print('this is a test')
        if purchase_amount <= self.balance:
            self.balance -= purchase_amount
            self.check_active()
            return True
        else:
            return False
    
    def check_active(self):
        print('called')
        if self.balance == 0:
            self.is_active = False
        else:
            self.is_active = True

    def refund(self, refund_amt):
        self.balance += refund_amt
        self.check_active()
        print(f'Refund Issued for ${refund_amt}')

    def create_card_num(self):
        cards_in_business = Card.objects.filter(business = self.business)
        self.card_num = len(cards_in_business) + 1


class Transaction(models.Model):
     amount = models.FloatField(default=0)
     created = models.DateTimeField(auto_now_add=True)
     gift_card = models.ForeignKey(Card, related_name='transactions', on_delete=models.SET_NULL,null=True)
     trans_type = models.CharField(max_length=25, null=True, unique=False, blank=True)
     
     def __str__(self):
        return f'Transaction #{self.id}'
     
    #  def send_receipt(self):
    #     send_mail(
    #         f"{self.trans_type.title()} RECEIPT #{self.id} DATE: {self.created} {self.trans_type}",
    #         f"Your {self.trans_type} for ${self.amount} was processed.",
    #         "atachart.changtroraleke@gmail.com",
    #         ["atachart.changtroraleke@gmail.com"],
    #         fail_silently=False,
    #     )

