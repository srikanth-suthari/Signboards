from django.urls import path
from . import views

app_name = 'signboards'

urlpatterns = [
    path('', views.signboard_home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('quote/', views.request_quote, name='quote'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('types/', views.signboard_types, name='types'),
    path('calculate-price/', views.calculate_price, name='calculate_price'),
]
