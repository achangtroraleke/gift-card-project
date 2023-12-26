from django.shortcuts import render, redirect
from .models import Card, Customer, Transaction
from .forms import CardForm, CustomerForm, TransactionForm
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def home(request):
    if request.method == "POST":
        search_item = request.POST.get('q','')
        hide_inactive = request.POST.get('is_active')
        cards = Card.objects.filter(
            Q(id__contains=search_item) |
            Q(customer__first_name__contains=search_item) |
            Q(customer__last_name__contains = search_item),
            )
        if hide_inactive:
            cards = cards.filter(is_active=hide_inactive)
        print(cards)
      
        context = {'cards': cards}
        return render(request, 'base/home.html', context = context)
    cards = Card.objects.all()

    context = {'cards': cards}
    return render(request, 'base/home.html', context= context)


def createPage(request):
    form = CardForm()
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            new_card = form.save(commit=False)
            new_card.original_balance = form.cleaned_data['balance']
            new_card.save()
            return redirect(f'/gift-card/{new_card.id}')
    context={'form':form}
    return render(request, 'base/card-form.html', context)

def createCustomer(request):
    form =CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create-card')
    context ={'form':form}
    return render(request, 'base/customer-form.html', context)

def cardPage(request, pk):
    card = Card.objects.get(id=pk)
    form = CardForm(instance=card)
    transactions = Transaction.objects.filter(gift_card = card,).order_by("created")
    
    context = {'form':form, 'card':card,'transactions': transactions}

    return render(request, 'base/card.html', context)

def purchasePage(request, pk):
    card = Card.objects.get(id=pk)
    form = TransactionForm()
    
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if float(form.data['total']) <= card.balance:
            if form.is_valid():
                print(form.cleaned_data)
                new_val = form.cleaned_data['total']
                if card.affordable(new_val):
                    new_transaction = Transaction(amount=new_val, gift_card=card, trans_type="purchase")
                    new_transaction.save()
                    card.save()
                return redirect(f'/gift-card/{pk}/')
        else:
            messages.error(request, f'Not enough funds.')
          
    context = {'form':form, 'card':card}
    return render(request, 'base/purchase.html', context)


def refundPage(request, pk):
    card = Card.objects.get(id=pk)
    form = TransactionForm()
    
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if float(form.data['total']) <= card.original_balance - card.balance:
            if form.is_valid():
                amt = form.cleaned_data['total']
                card.refund(amt)
                card.check_active()
                new_transaction = Transaction(amount = amt, gift_card=card, trans_type="refund")
                card.save()
                new_transaction.save()
                return redirect(f'/gift-card/{pk}/')
        else:
            messages.error(request, f'Cannot refund more than original balance (${card.original_balance}).')
          
    context = {'form':form, 'card':card, 'refund':True}
    return render(request, 'base/purchase.html', context)

def customerPage(request, pk):
    customer = Customer.objects.get(id=pk)
    gift_cards = Card.objects.filter(customer = customer)

    context = {'customer':customer, 'cards': gift_cards}
    return render(request, 'base/customer-page.html', context)

