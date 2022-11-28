from django.shortcuts import render

import razorpay
from food_site.settings import RZP_KEY_ID, RZP_KEY_SECRET
# Create your views here.
# def cart(request):
#     return render(request, 'marketplace/cart.html')

client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

DATA = {
    "amount": 100, #100 paise = rs 1
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "value3",
        "key2": "value2"
    }
}

rzp_order = client.order.create(data=DATA)
print(rzp_order)

