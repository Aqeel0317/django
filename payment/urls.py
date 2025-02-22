from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('easypaisa/', views.easypaisa_process, name='easypaisa_process'),
    path('easypaisa_callback/', views.easypaisa_callback, name='easypaisa_callback'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('error/', views.payment_error, name='payment_error'),
]
