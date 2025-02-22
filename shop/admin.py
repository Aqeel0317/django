from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from .models import Product, Category, ProductImage, SaleAnnouncement

class CustomAdminSite(admin.AdminSite):
    site_header = "My Custom Admin"
    site_title = "Admin Panel"
    index_title = "Welcome to My Custom Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name="dashboard"),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        active_sales = SaleAnnouncement.objects.filter(active=True).count()

        context = {
            "total_products": total_products,
            "total_categories": total_categories,
            "active_sales": active_sales
        }
        # Render your custom dashboard template (ensure you create this file)
        return render(request, "admin/dashboard.html", context)

admin_site = CustomAdminSite(name="custom_admin")

# Register models with your custom admin site
admin_site.register(Product)
admin_site.register(Category)
admin_site.register(ProductImage)
admin_site.register(SaleAnnouncement)
