from django.shortcuts import render

from orders.forms import OrderForm

# Create your views here.
def cart(request):
    return render(request, 'marketplace/cart.html')

def search(request):
    return render(request, 'marketplace/search.html')

def checkout(request):
    form = OrderForm()
    context={
        'form':form,
    }
    return render(request, 'marketplace/checkout.html',context)
