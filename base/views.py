from django.shortcuts import render, redirect
from .models import Card, Customer
from .forms import CardForm, CustomerForm, PurchaseForm


# Create your views here.

def home(request):
    cards = Card.objects.all()

    context = {'cards': cards}
    return render(request, 'base/home.html', context= context)

def createPage(request):
    form = CardForm()
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
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
    context = {'form':form, 'card':card}

    return render(request, 'base/card.html', context)

def purchagePage(request, pk):
    card = Card.objects.get(id=pk)
    form = PurchaseForm()
    
    context = {'form':form, 'card':card}
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        obj_to_update = CardForm(request.POST, instance=card)
        if form.is_valid():
            print(form.cleaned_data)
            new_val = form.cleaned_data['total']
            card.amount -= new_val
            card.save()
            
            
            return redirect('home')

    return render(request, 'base/purchase.html', context)
    