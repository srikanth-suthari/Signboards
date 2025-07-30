from django.urls import path
from . import views

app_name = 'vegetables'

urlpatterns = [
    path('', views.vegetable_list, name='list'),
    path('category/<int:category_id>/', views.vegetables_by_category, name='by_category'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:vegetable_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]
