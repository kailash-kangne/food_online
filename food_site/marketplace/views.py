from django.shortcuts import render, get_object_or_404
from menu.models import Category , FoodItem
from vendor.models import Vendor
from orders.forms import OrderForm

from django.db.models import Prefetch


# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            "fooditems",
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )#reverse lookup

    context={
        'vendor': vendor,
        'categories': categories,
    }
    return render(request, 'marketplace/vendor_detail.html',context)


# def cart(request):
#     return render(request, 'marketplace/cart.html')

# def search(request):
#     return render(request, 'marketplace/search.html')

# def checkout(request):
#     form = OrderForm()
#     context={
#         'form':form,
#     }
#     return render(request, 'marketplace/checkout.html',context)
