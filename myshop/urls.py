from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from paypal.standard.ipn.views import ipn
# Import your custom admin site instance
from shop.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),  # Use your custom admin site
    path('payment/', include('payment.urls', namespace='payment')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('', include(('shop.urls', 'shop'), namespace='shop')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('paypal/', include(('paypal.standard.ipn.urls', 'paypal'), namespace='paypal')),
    path('paypal/ipn/', ipn, name='paypal-ipn'),
    path('about/', include(('shop.urls', 'shop'), namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
