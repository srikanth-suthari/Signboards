from django.urls import path
from . import views

app_name = 'contractors'

urlpatterns = [
    path('', views.contractor_list, name='list'),
    path('<int:contractor_id>/', views.contractor_detail, name='detail'),
    path('<int:contractor_id>/book/', views.book_contractor, name='book'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('categories/', views.category_list, name='categories'),
    path('categories/<int:category_id>/', views.contractors_by_category, name='by_category'),
]
