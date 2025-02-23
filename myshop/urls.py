from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from paypal.standard.ipn.views import ipn
# Import your custom admin site instance
from django.views.static import serve
from shop.admin import admin_site
from django.urls import re_path
from django.views.static import serve
from django.conf import settings


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

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
