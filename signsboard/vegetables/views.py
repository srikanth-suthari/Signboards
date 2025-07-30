from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Vegetable, VegetableCategory, Cart, CartItem, VegetableOrder, OrderItem, DeliverySlot
from .forms import CheckoutForm
import uuid

def vegetable_list(request):
    vegetables = Vegetable.objects.filter(is_available=True)
    categories = VegetableCategory.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        vegetables = vegetables.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        vegetables = vegetables.filter(category_id=category_id)
    
    # Organic filter
    organic_only = request.GET.get('organic')
    if organic_only == '1':
        vegetables = vegetables.filter(is_organic=True)
    
    context = {
        'vegetables': vegetables,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
        'organic_only': organic_only == '1',
    }
    return render(request, 'vegetables/list.html', context)

def vegetables_by_category(request, category_id):
    category = get_object_or_404(VegetableCategory, id=category_id)
    vegetables = Vegetable.objects.filter(category=category, is_available=True)
    return render(request, 'vegetables/by_category.html', {
        'category': category,
        'vegetables': vegetables
    })

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total = sum(item.total_price for item in cart_items)
    return render(request, 'vegetables/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    quantity = float(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        vegetable=vegetable,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{vegetable.name} added to cart!')
    return redirect('vegetables:cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('vegetables:cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = float(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('vegetables:cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('vegetables:cart')
    
    delivery_slots = DeliverySlot.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = VegetableOrder.objects.create(
                customer=request.user,
                order_number=f'VEG{uuid.uuid4().hex[:8].upper()}',
                delivery_address=form.cleaned_data['delivery_address'],
                delivery_phone=form.cleaned_data['delivery_phone'],
                delivery_slot=form.cleaned_data['delivery_slot'],
                delivery_date=form.cleaned_data['delivery_date'],
                special_instructions=form.cleaned_data['special_instructions'],
            )
            
            # Create order items
            total_amount = 0
            for cart_item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    vegetable=cart_item.vegetable,
                    quantity=cart_item.quantity,
                    price_per_unit=cart_item.vegetable.price_per_unit
                )
                total_amount += order_item.total_price
            
            # Update order total
            order.total_amount = total_amount
            order.save()
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, f'Order placed successfully! Order number: {order.order_number}')
            return redirect('vegetables:order_detail', order_id=order.id)
    else:
        form = CheckoutForm()
    
    total = sum(item.total_price for item in cart_items)
    
    return render(request, 'vegetables/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'delivery_slots': delivery_slots,
    })

@login_required
def my_orders(request):
    orders = VegetableOrder.objects.filter(customer=request.user)
    return render(request, 'vegetables/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(VegetableOrder, id=order_id, customer=request.user)
    return render(request, 'vegetables/order_detail.html', {'order': order})
