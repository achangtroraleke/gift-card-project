from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name ='home'),
    path('/create-card', views.createPage, name='create-card'),
    path('/create-customer', views.createCustomer, name='create-customer')
]