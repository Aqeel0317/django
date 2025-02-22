from .models import SaleAnnouncement

def sale_announcements(request):
    active_sales = SaleAnnouncement.objects.filter(active=True)
    for sale in active_sales:
        if sale.background_color.startswith('#'):
            sale.background_color = sale.background_color[1:]  # Remove the '#' symbol
    return {'active_sales': active_sales}

