from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('', views.vehicle_list, name='list'),
    path('book/', views.book_vehicle, name='book'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('types/', views.vehicle_types, name='types'),
    path('calculate-fare/', views.calculate_fare, name='calculate_fare'),
]
