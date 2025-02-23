from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

   

# Product Model (main product model)
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)  # Main image
    description = RichTextField(blank=True, null=True)
    specifications = models.TextField(blank=True)  # New field for product specifications
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True) 

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        return self.name

# Product Image Model (for additional images)
# models.py
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d')

    def __str__(self):
        return f"Image for {self.product.name}"


class SaleAnnouncement(models.Model):
    SALE_TYPES = [
        ('discount', 'Discount'),
        ('special_offer', 'Special Offer'),
        ('summer_sale', 'Summer Sale'),
        ('flash_sale', 'Flash Sale'),
        ('clearance', 'Clearance'),
    ]
    
    message = models.CharField(max_length=255, help_text="Short message for the sale (e.g., '20% OFF').")
    sale_type = models.CharField(max_length=20, choices=SALE_TYPES, default='discount')
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True, help_text="Leave empty for ongoing sale.")
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Discount percentage or amount (e.g., '20%' or '$40').")
    image = models.ImageField(upload_to='sale_images/', null=True, blank=True, help_text="Image for the sale banner.")
    background_color = models.CharField(max_length=7, default="#ff5722", help_text="Background color of the banner (in hex, e.g., #ff5722).")

    def __str__(self):
        return f"{self.sale_type} - {self.message[:30]}"  # Display first 30 characters of the message

    def is_active(self):
        from django.utils import timezone
        if self.end_date:
            return self.active and self.start_date <= timezone.now() <= self.end_date
        return self.active and self.start_date <= timezone.now()

    def get_discount_text(self):
        """Returns the discount text (e.g., '20% off', '$40 off', etc.)."""
        if self.discount:
            if self.discount < 100:  # assuming it's a percentage discount
                return f"{self.discount}% OFF"
            else:
                return f"${self.discount} OFF"
        return ""
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subject} from {self.name}"
