from django.urls import path, re_path

from stocks import views

urlpatterns = [
    path('symbol/', views.symbol_list),
    re_path(r'analysis$', views.symbol_detail),
]