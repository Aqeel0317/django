from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from orders.models import Order

def easypaisa_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    # Build payload for Easypaisa API based on their documentation
    payload = {
        'amount': str(float(order.get_total_cost())),
        'transaction_id': str(order.id),
        'callback_url': f'http://{host}{reverse("payment:easypaisa_callback")}',
        # Add additional fields required by Easypaisa here
    }

    # Easypaisa API endpoint (update this with the actual URL)
    easypaisa_api_url = "https://api.easypaisa.com.pk/payment/initiate"

    try:
        response = requests.post(easypaisa_api_url, data=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Easypaisa API error:", e)
        return redirect('payment:payment_error')

    data = response.json()
    payment_url = data.get('payment_url')
    if not payment_url:
        return redirect('payment:payment_error')

    return redirect(payment_url)

def easypaisa_callback(request):
    # Retrieve necessary parameters from the callback
    transaction_id = request.GET.get('transaction_id')
    status = request.GET.get('status')

    try:
        order = Order.objects.get(id=transaction_id)
    except Order.DoesNotExist:
        return render(request, 'payment/error.html', {'message': 'Order not found.'})

    if status == 'success':
        order.paid = True
        order.save()
        return redirect(reverse('payment:done'))
    else:
        return redirect(reverse('payment:canceled'))

def payment_error(request):
    return render(request, 'payment/error.html', {'message': 'There was an error processing your payment.'})

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(float(order.get_total_cost())),  # Convert to float, then to string
        'item_name': f'Order {order.id}',
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("payment:done")}',
        'cancel_return': f'http://{host}{reverse("payment:canceled")}',
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'order': order, 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
