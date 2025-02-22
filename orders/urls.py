from django.urls import path
from . import views
urlpatterns = [
    path('create/',views.order_create,name='order_create'),
    path('track/', views.order_tracking, name='order_tracking'),
    ]