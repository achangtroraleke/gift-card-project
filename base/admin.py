from django.contrib import admin

from .models import Card, Customer, Transaction, MyCustomUser, Business
# Register your models here.

admin.site.register(Card)
admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(MyCustomUser)
admin.site.register(Business)