from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name ='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout' ),

    path('customer/<str:pk>', views.customerPage, name='customer-page'),
    path('create-customer', views.createCustomer, name='create-customer'),
    
    path('gift-card/<str:pk>/', views.cardPage, name='card-page'),
    path('gift-card/<str:pk>/redeem', views.purchasePage, name='purchase'),
    path('gift-card/<str:pk>/refund/', views.refundPage, name='refund'),
   
 
    path('user/dashboard', views.businessPage, name='dashboard'),
    path('user/profile', views.profilePage, name='profile'),
    path('user/profile/edit', views.profileEditPage, name='profile-edit'),

    path('business/new', views.createBusinessPage, name='new-business'),
    path('business/<str:pk>/giftcards', views.getAllCards, name='get-business-cards'),
    path('business/<str:pk>/edit', views.editBusinessPage, name='edit-business'),
    path('business/<str:pk>/create-card', views.createCardPage, name='create-card'),
]