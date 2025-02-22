from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductImage
from cart.forms import CartAddProductForm
from django.db.models import Q

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/product/list.html', context)

def product_search(request):
    query = request.GET.get('query')
    categories = Category.objects.all()  # Provide categories for the header
    results = []
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            available=True
        )
    context = {
        'query': query,
        'results': results,
        'categories': categories
    }
    return render(request, 'shop/product/search.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    images = product.images.all()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    categories = Category.objects.all()  # Include categories for consistent header
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'images': images,
        'related_products': related_products,
        'specifications': product.specifications,  # Pass specifications to template
        'categories': categories,
    }
    return render(request, 'shop/product/detail.html', context)

def about(request):
    categories = Category.objects.all()  # Pass categories so header navigation works
    context = {
        'categories': categories
    }
    return render(request, 'shop/about.html', context)
from django.shortcuts import render, redirect
from .forms import ContactMessageForm
from .models import Category  # for header navigation, if needed

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, you can add a success message here
            return redirect('shop:contact')  # or redirect to a thank-you page
    else:
        form = ContactMessageForm()
    
    # Pass categories if your base template expects them for navigation
    categories = Category.objects.all()
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'shop/contact.html', context)
