from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('card-modal/', views.card_modal, name='card_modal'),
    path('create/', views.create, name='create'),
    path('transaction-form/', views.transaction_form, name='transaction_form'),
    path('card/<str:card_number>/', views.card, name='card'),
]
