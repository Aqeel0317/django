from django.urls import path
from . import views
from .views import about
app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.product_search, name='product_search'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('categories/', views.category_list, name='category_list'),
    path('<slug:category_slug>/', views.product_list,name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
   



]
