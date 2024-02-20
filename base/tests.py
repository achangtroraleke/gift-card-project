from django.test import TestCase
from .models import MyCustomUser, Customer, Card, Business

# Create your tests here.

class CustomerTestCase(TestCase):
    def setUp(self):
        test_profile = MyCustomUser.objects.create(name='user', email='user@gmail.com', password='test')
        Customer.objects.create(first_name='test', last_name='customer', created_by=test_profile)

    def tearDown(self):
        test_profile = MyCustomUser.objects.get(email='user@gmail.com')
        test_profile.delete()
        test_customer = Customer.objects.get(first_name='test')
        test_customer.delete()

    def test_customer_is_created(self):
        test_customer = Customer.objects.get(first_name='test')
        self.assertEqual(test_customer.first_name, 'test' )
        self.assertEqual(test_customer.last_name, 'customer' )

class CardTestCase(TestCase):
    def setUp(self):
        test_profile = MyCustomUser.objects.create(name='user', email='user@gmail.com', password='test')
        test_bus = Business.objects.create(name='test_bus', owner=test_profile)
        test_customer = Customer.objects.create(first_name='test', last_name='customer', created_by=test_profile)
        Card.objects.create(id=1, original_balance=100, balance=100, customer=test_customer, business=test_bus)
    
    def test_card_is_created(self):
        test_card = Card.objects.get(id=1)
        self.assertEqual(test_card.original_balance, 100)

    def test_card_used(self):
        test_card = Card.objects.get(id=1)
        result = test_card.affordable(50)
        self.assertTrue(result)

    def test_card_insufficient_funds(self):
        test_card = Card.objects.get(id=1)
        result = test_card.affordable(900)
        self.assertFalse(result)
        
    def test_card_turns_inactive_with_no_funds(self):
        test_card = Card.objects.get(id=1)
        test_card.balance = 0
        test_card.check_active()
        self.assertFalse(test_card.is_active)

    def test_card_format_ending_zero_to_string(self):
        test_card = Card.objects.get(id=1)
        result = test_card.format_to_money(2.0)
        self.assertEqual(result, '2.00')

    

