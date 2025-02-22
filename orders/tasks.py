from celery import shared_task
from django.core.mail import send_mail
from .models import Order
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def order_created(order_id):
    """
    Task to send an email notification when an order is
    successfully created, and place the order with CJ Dropshipping.
    """
    try:
        order = Order.objects.get(id=order_id)
        
        # 1. Send the confirmation email
        subject = f'Order nr. {order.id}'
        message = f'Dear {order.first_name},\n\nYou have successfully placed an order. Your order id is {order.id}.'
        mail_sent = send_mail(subject, message, 'aqeel03319384502@gmail.com', [order.email])
        
        # 2. Prepare the data for CJ Dropshipping API
        order_data = {
            'user_id': settings.CJ_USER_ID,
            'api_key': settings.CJ_API_KEY,
            'order_id': order.id,
            'email': order.email,
            'address': order.address,
            'postal_code': order.postal_code,
            'city': order.city,
            'first_name': order.first_name,
            'last_name': order.last_name,
            'items': [
                {
                    'product_sku': item.product.sku,  # Assuming you have a 'sku' field in Product model
                    'quantity': item.quantity,
                    'price': str(item.price),
                }
                for item in order.items.all()
            ]
        }
        
        # 3. Send the order to CJ Dropshipping API
        cj_api_url = 'https://api.cjdropshipping.com/api/order/create'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.CJ_API_SECRET}'
        }
        
        try:
            response = requests.post(cj_api_url, json=order_data, headers=headers)
            response_data = response.json()

            # Check the response and update the order
            if response.status_code == 200 and response_data['status'] == 'success':
                # Add any additional information from CJ API response, like tracking number
                order.status = 'processing'
                order.save()
                
                # Log the successful order creation
                logger.info(f"Order {order.id} successfully created with CJ Dropshipping.")
            else:
                logger.error(f"Failed to create order with CJ Dropshipping. Response: {response_data}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during CJ Dropshipping API call: {e}")
        
        return mail_sent

    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist.")
        return None
    except Exception as e:
        logger.error(f"An error occurred while sending the order confirmation email: {e}")
        return None
