from django.urls import path, re_path

from stocks import views

urlpatterns = [
    path('symbol/', views.symbol_list),
    re_path(r'analysis2$', views.symbol_detail),
    path('analysis/example', views.example),
    path(r'analysis', views.matt),
]
