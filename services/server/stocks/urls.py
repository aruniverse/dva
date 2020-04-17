from django.urls import path

from stocks import views

urlpatterns = [
    path('api/symbol/', views.symbol_list),
    path('api/symbol/<int:pk>/', views.symbol_detail),
]
