from django.db import models

# Create your models here.



class Customer(models.Model):
    f_name = models.CharField(max_length=25, null=True, blank=True, unique=False)
    l_name = models.CharField(max_length=25, null=True, blank=True, unique=False)
    
    def __str__(self):
        return f'{self.f_name} {self.l_name} '
    
class Card(models.Model):
    amount = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)   
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Customer, related_name='gift_cards', on_delete=models.SET_NULL, null=True)

    