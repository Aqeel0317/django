from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.shortcuts import get_object_or_404, redirect
from .models import Order
from .tasks import order_created
from django.urls import reverse
from .models import Order
from decimal import Decimal

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Create order instance without saving immediately
            order = form.save(commit=False)
            # Set shipping fee based on country
            if form.cleaned_data['country'].strip().lower() == 'pakistan':
                order.shipping_fee = Decimal('0.00')
            else:
                order.shipping_fee = Decimal('10.00')  # Example fee for non-Pakistani orders
            order.save()
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            request.session['order_id'] = order.id
            # Optionally, store the chosen payment method in session:
            request.session['payment_method'] = form.cleaned_data.get('payment_method')
            order_created.delay(order.id)
            cart.clear()

            # Redirect based on payment method
            payment_method = form.cleaned_data.get('payment_method')
            if payment_method == 'easypaisa':
                return redirect(reverse('payment:easypaisa_process'))
            else:
                return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})



def order_tracking(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                return render(request, 'orders/order/tracking.html', {'order': order})
            except Order.DoesNotExist:
                return render(request, 'orders/order/tracking.html', {'error': 'Order not found'})
    return redirect(reverse('shop:product_list'))  # Redirect to home if no POST data
    
                 

 #clear the cart
# launch asynchronous task