from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import SignboardType, SignboardSize, SignboardFinish, SignboardOrder, SignboardGallery
from .forms import SignboardQuoteForm
import uuid

def signboard_home(request):
    featured_gallery = SignboardGallery.objects.filter(is_featured=True)[:6]
    signboard_types = SignboardType.objects.all()
    return render(request, 'signboards/home.html', {
        'featured_gallery': featured_gallery,
        'signboard_types': signboard_types
    })

def gallery(request):
    gallery_items = SignboardGallery.objects.all()
    signboard_types = SignboardType.objects.all()
    
    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        gallery_items = gallery_items.filter(signboard_type_id=type_filter)
    
    return render(request, 'signboards/gallery.html', {
        'gallery_items': gallery_items,
        'signboard_types': signboard_types,
        'selected_type': int(type_filter) if type_filter else None,
    })

@login_required
def request_quote(request):
    if request.method == 'POST':
        form = SignboardQuoteForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.order_number = f'SB{uuid.uuid4().hex[:8].upper()}'
            order.save()
            
            # Calculate pricing
            order.calculate_total_cost()
            order.save()
            
            messages.success(request, f'Quote request submitted! Order number: {order.order_number}')
            return redirect('signboards:order_detail', order_id=order.id)
    else:
        form = SignboardQuoteForm()
    
    return render(request, 'signboards/quote.html', {'form': form})

@login_required
def my_orders(request):
    orders = SignboardOrder.objects.filter(customer=request.user)
    return render(request, 'signboards/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(SignboardOrder, id=order_id, customer=request.user)
    return render(request, 'signboards/order_detail.html', {'order': order})

def signboard_types(request):
    types = SignboardType.objects.all()
    return render(request, 'signboards/types.html', {'types': types})

def calculate_price(request):
    if request.method == 'GET':
        type_id = request.GET.get('type_id')
        size_id = request.GET.get('size_id')
        finish_id = request.GET.get('finish_id')
        urgency = request.GET.get('urgency', 'standard')
        
        try:
            signboard_type = SignboardType.objects.get(id=type_id)
            size = SignboardSize.objects.get(id=size_id)
            
            base_cost = signboard_type.price_per_sqft * size.area_sqft
            
            # Apply finish cost
            if finish_id:
                finish = SignboardFinish.objects.get(id=finish_id)
                finish_cost = base_cost * (finish.additional_cost_percentage / 100)
                base_cost += finish_cost
            
            # Apply urgency charges
            urgency_multiplier = {
                'standard': 0,
                'urgent': 0.25,
                'express': 0.50
            }
            urgency_charges = base_cost * urgency_multiplier.get(urgency, 0)
            
            total_cost = base_cost + urgency_charges
            
            return JsonResponse({
                'success': True,
                'base_cost': float(base_cost),
                'urgency_charges': float(urgency_charges),
                'total_cost': float(total_cost)
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
