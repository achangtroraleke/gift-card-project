from django.shortcuts import render, redirect, get_object_or_404
from .models import Card, Customer, Transaction, MyCustomUser, Business
from .forms import CardForm, CustomerForm, TransactionForm, MyUserCreationForm, UserLoginForm, NewBusinessForm, EditUserForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'base/home.html')

"""Card Views"""
@login_required(login_url='/login')
def getAllCards(request, pk):
    sel_business = Business.objects.get(id=pk)

    if request.method == "POST":
        search_item = request.POST.get('q','')
        hide_inactive = request.POST.get('is_active')
        cards = Card.objects.filter(
            Q(card_num__contains=search_item) |
            Q(customer__first_name__contains=search_item) |
            Q(customer__last_name__contains = search_item),
            business = sel_business.id
            )
        if hide_inactive:
            cards = cards.filter(is_active=hide_inactive)
        context = {'cards': cards, 'business':sel_business}
        return render(request, 'base/table.html', context = context)
    cards = Card.objects.filter(business=sel_business)
    context = {'cards': cards, 'business':sel_business} 
    return render(request, 'base/table.html', context= context)
    


@login_required(login_url='/')
def createCardPage(request, pk):
    form = CardForm()
    sel_business = Business.objects.get(id=pk)
    form.fields['customer'].queryset = Customer.objects.filter(created_by = request.user)
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            new_card = form.save(commit=False)
            new_card.original_balance = form.cleaned_data['balance']
            new_card.business = sel_business
            new_card.create_card_num()
            new_card.save()
            sel_business.gc_total_bal += form.cleaned_data['balance']
            sel_business.save()
            return redirect(f'/gift-card/{new_card.id}')
    context={'form':form, 'business':sel_business}
    return render(request, 'card/card-form.html', context)


@login_required(login_url='/')
def cardPage(request, pk):
    card = get_object_or_404(Card, id=pk)
    form = CardForm(instance=card)
    transactions = Transaction.objects.filter(gift_card = card,).order_by("created")
    context = {'form':form, 'card':card,'transactions': transactions}
    return render(request, 'card/card.html', context)

@login_required(login_url='/')
def purchasePage(request, pk):
    card = get_object_or_404(Card, id=pk)
    form = TransactionForm()
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if float(form.data['total']) <= card.balance:
            if form.is_valid():
                new_val = form.cleaned_data['total']
                if card.affordable(new_val):
                    new_transaction = Transaction(amount=new_val, gift_card=card, trans_type="purchase")
                    new_transaction.save()
                    card.save()
                    messages.success(request, 'Purchase Successful!')
                    
        else:
            messages.error(request, f'Not enough funds.')      
    context = {'form':form, 'card':card}
    return render(request, 'card/purchase.html', context)

@login_required(login_url='/')
def refundPage(request, pk):
    card = get_object_or_404(Card, id=pk)
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
            formatted_balance = card.format_to_money(card.original_balance)
            messages.error(request, f'Cannot refund more than original balance (${formatted_balance}).')
    context = {'form':form, 'card':card, 'refund':True}
    return render(request, 'card/purchase.html', context)

""" Customer Views """
@login_required(login_url='/')
def createCustomer(request):
    form =CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            new_customer = form.save(commit=False)
            new_customer.created_by = request.user
            new_customer.save()
            return redirect('/')
    context ={'form':form}
    return render(request, 'customer/customer-form.html', context)

@login_required(login_url='/')
def customerPage(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    gift_cards = Card.objects.filter(customer = customer)

    context = {'customer':customer, 'cards': gift_cards}
    return render(request, 'customer/customer-page.html', context)

""" User Views"""

def register(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('/')

    context = {'form': form}
    return render (request, 'user/register.html', context )

def loginPage(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        email = form.data['email']
        pw = form.data['password']
        user = authenticate(username = email, password = pw)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect e-mail or password.')
    context ={'form':form}
    return render(request, 'user/login.html', context)

def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')

@login_required(login_url='/login')
def profilePage(request):
    edit = False    
    context = {'edit':edit, }
    return render( request,  'user/profile.html', context)

@login_required(login_url='/login')
def profilePage(request):
    edit = False    
    context = {'edit':edit, }
    return render( request,  'user/profile.html', context)

@login_required(login_url='/login')
def profileEditPage(request):
    edit = True    
    form = EditUserForm(instance=request.user)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'edit':edit, 'form':form}
    return render( request,  'user/profile.html', context)
    

""" Business views """

@login_required(login_url=('/'))
def createBusinessPage(request):
    form = NewBusinessForm()
    if request.method == 'POST':
        form = NewBusinessForm(request.POST)
        if form.is_valid():
            new_business = form.save(commit=False)
            new_business.owner = request.user
            new_business.save()
            return redirect('/user/dashboard')
    context = {'form': form}
    return render(request, 'business/new_business.html', context)

@login_required(login_url='/')
def businessPage(request):
    user_businesses = Business.objects.filter(owner = request.user)
    context = {'businesses':user_businesses}
    return render(request, 'business/dashboard-page.html', context)

@login_required(login_url=('/'))
def editBusinessPage(request, pk):
    sel_business = Business.objects.get(id=pk)
    form = NewBusinessForm(instance=sel_business)
    if request.method == 'POST':
        form = NewBusinessForm(request.POST,request.FILES, instance = sel_business)
        if form.is_valid():
            edit_business = form.save(commit=False)
            new_img=form.cleaned_data['business_image']
            edit_business.bus_img = new_img
            edit_business.owner = request.user
            edit_business.save()
            return redirect('get-business-cards', pk=sel_business.id)
    context = {'form': form}
    return render(request, 'business/business-page.html', context)
