from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.



class Customer(models.Model):
    first_name = models.CharField(max_length=25, null=True, blank=True, unique=False)
    last_name = models.CharField(max_length=25, null=True, blank=True, unique=False)
    
    def __str__(self):
        return f'{self.first_name.title()} {self.last_name.title()} '
    
class Card(models.Model):
    original_balance = models.FloatField(default=0)
    balance = models.FloatField(default=0, validators=[MinValueValidator(0)])
    updated = models.DateTimeField(auto_now=True)   
    created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, related_name='gift_cards', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)


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




class Transaction(models.Model):
     amount = models.FloatField(default=0)
     created = models.DateTimeField(auto_now_add=True)
     gift_card = models.ForeignKey(Card, related_name='transactions', on_delete=models.SET_NULL,null=True)
     trans_type = models.CharField(max_length=25, null=True, unique=False, blank=True)
     def __str__(self):
        return f'Transaction #{self.id}'