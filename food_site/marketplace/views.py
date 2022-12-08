from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponse, JsonResponse

from menu.models import Category , FoodItem
from vendor.models import Vendor
from .models import Cart

from orders.forms import OrderForm

from django.db.models import Prefetch

from .context_preprocessors import get_cart_counter


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

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context={
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html',context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def add_to_cart(request, food_id):

    if request.user.is_authenticated:
        if is_ajax(request=request):
            
            #check if food item exist
            try:
                fooditem= FoodItem.objects.get(id=food_id)
                #check if user has already added  that food to cart  
                try:
                    chkCart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    #increase cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'success', 'message':'increased cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
                except:
                    chkCart = Cart.objects.create(user=request.user,fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success', 'message':'added food to cart','cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
            except:
                return JsonResponse({'status': 'failed', 'message':'this food not exist'})
                
        else:
            return JsonResponse({'status': 'failed', 'message':'invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message':'plz log in to continue'})

def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            
            #check if food item exist
            try:
                fooditem= FoodItem.objects.get(id=food_id)
                #check if user has already added  that food to cart  
                try:
                    chkCart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    #decrease cart quantity
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'success', 'message':'decreased cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
                except:
                    
                    return JsonResponse({'status': 'failed', 'message':'you dont have item in cart'})
            except:
                return JsonResponse({'status': 'failed', 'message':'this food not exist'})
                
        else:
            return JsonResponse({'status': 'failed', 'message':'invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message':'plz log in to continue'})


def delete_cart(request):
     return render(request, 'marketplace/delete_cart.html')

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context={
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html',context)




# def search(request):
#     return render(request, 'marketplace/search.html')

def checkout(request):
    form = OrderForm()
    context={
        'form':form,
    }
    return render(request, 'marketplace/checkout.html',context)
