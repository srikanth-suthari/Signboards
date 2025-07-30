from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Contractor, ContractorCategory, ContractorBooking
from .forms import ContractorBookingForm

def contractor_list(request):
    contractors = Contractor.objects.filter(is_available=True)
    categories = ContractorCategory.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        contractors = contractors.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        contractors = contractors.filter(category_id=category_id)
    
    context = {
        'contractors': contractors,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'contractors/list.html', context)

def contractor_detail(request, contractor_id):
    contractor = get_object_or_404(Contractor, id=contractor_id)
    return render(request, 'contractors/detail.html', {'contractor': contractor})

@login_required
def book_contractor(request, contractor_id):
    contractor = get_object_or_404(Contractor, id=contractor_id)
    
    if request.method == 'POST':
        form = ContractorBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.contractor = contractor
            booking.save()
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('contractors:booking_detail', booking_id=booking.id)
    else:
        form = ContractorBookingForm()
    
    return render(request, 'contractors/book.html', {
        'contractor': contractor,
        'form': form
    })

@login_required
def my_bookings(request):
    bookings = ContractorBooking.objects.filter(customer=request.user)
    return render(request, 'contractors/my_bookings.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(ContractorBooking, id=booking_id, customer=request.user)
    return render(request, 'contractors/booking_detail.html', {'booking': booking})

def category_list(request):
    categories = ContractorCategory.objects.all()
    return render(request, 'contractors/categories.html', {'categories': categories})

def contractors_by_category(request, category_id):
    category = get_object_or_404(ContractorCategory, id=category_id)
    contractors = Contractor.objects.filter(category=category, is_available=True)
    return render(request, 'contractors/by_category.html', {
        'category': category,
        'contractors': contractors
    })
