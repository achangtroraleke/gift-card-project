from django.shortcuts import render, redirect
from .models import Card, Customer
from .forms import CardForm, CustomerForm


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

