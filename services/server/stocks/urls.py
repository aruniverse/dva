from django.urls import path

from stocks import views

urlpatterns = [
    path('symbol/', views.symbol_list),
    path('symbol/<int:pk>/', views.symbol_detail),
]