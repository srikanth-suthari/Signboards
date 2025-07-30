from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Vehicle, VehicleType, VehicleBooking, Driver
from .forms import VehicleBookingForm
import uuid

def vehicle_list(request):
    vehicles = Vehicle.objects.filter(is_available=True)
    vehicle_types = VehicleType.objects.all()
    
    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        vehicles = vehicles.filter(vehicle_type_id=type_filter)
    
    # Filter by fuel type
    fuel_filter = request.GET.get('fuel')
    if fuel_filter:
        vehicles = vehicles.filter(fuel_type=fuel_filter)
    
    # Filter by AC
    ac_filter = request.GET.get('ac')
    if ac_filter == '1':
        vehicles = vehicles.filter(ac_available=True)
    
    context = {
        'vehicles': vehicles,
        'vehicle_types': vehicle_types,
        'selected_type': int(type_filter) if type_filter else None,
        'selected_fuel': fuel_filter,
        'ac_only': ac_filter == '1',
        'fuel_choices': Vehicle.FUEL_CHOICES,
    }
    return render(request, 'vehicles/list.html', context)

@login_required
def book_vehicle(request):
    if request.method == 'POST':
        form = VehicleBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.booking_number = f'VH{uuid.uuid4().hex[:8].upper()}'
            booking.save()
            
            # Calculate fare
            booking.calculate_fare()
            booking.save()
            
            messages.success(request, f'Booking request submitted! Booking number: {booking.booking_number}')
            return redirect('vehicles:booking_detail', booking_id=booking.id)
    else:
        form = VehicleBookingForm()
    
    return render(request, 'vehicles/book.html', {'form': form})

@login_required
def my_bookings(request):
    bookings = VehicleBooking.objects.filter(customer=request.user)
    return render(request, 'vehicles/my_bookings.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(VehicleBooking, id=booking_id, customer=request.user)
    return render(request, 'vehicles/booking_detail.html', {'booking': booking})

def vehicle_types(request):
    types = VehicleType.objects.all()
    return render(request, 'vehicles/types.html', {'types': types})

def calculate_fare(request):
    if request.method == 'GET':
        vehicle_id = request.GET.get('vehicle_id')
        booking_type = request.GET.get('booking_type')
        distance_km = float(request.GET.get('distance_km', 0))
        duration_hours = float(request.GET.get('duration_hours', 0))
        
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle_type = vehicle.vehicle_type
            
            base_fare = 100  # Base booking fee
            distance_fare = distance_km * vehicle_type.base_rate_per_km
            
            if booking_type == 'hourly':
                time_fare = duration_hours * vehicle_type.base_rate_per_hour
            else:
                time_fare = 0
            
            # Additional charges for airport transfers
            additional_charges = 200 if booking_type == 'airport_transfer' else 0
            
            total_fare = base_fare + distance_fare + time_fare + additional_charges
            
            return JsonResponse({
                'success': True,
                'base_fare': float(base_fare),
                'distance_fare': float(distance_fare),
                'time_fare': float(time_fare),
                'additional_charges': float(additional_charges),
                'total_fare': float(total_fare)
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
