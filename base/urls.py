from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name ='home'),
    path('create-card', views.createPage, name='create-card'),
    path('create-customer', views.createCustomer, name='create-customer'),
    path('gift-card/<str:pk>/', views.cardPage, name='card-page'),
    path('gift-card/<str:pk>/redeem', views.purchasePage, name='purchase'),
    path('gift-card/<str:pk>/refund/', views.refundPage, name='refund'),
    path('customer/<str:pk>', views.customerPage, name='customer-page'),
]