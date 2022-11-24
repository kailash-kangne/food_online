from django.shortcuts import render, redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages

# Create your views here.
def registerUser(request):

    if request.method == 'POST':
        #print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            #password is hashed
            password = form.cleaned_data['password']
            user = form.save(commit = False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()

            messages.success(request, "YOUR ACCOUNT HAS BEEN REGISTERED SUCCESSFULY")
            return redirect('registerUser')
        else:
            print("form not valid")
            print(form.errors)
            
    else:
        form= UserForm()
    context={
        'form': form,
    }
    return render(request,'accounts/registerUser.html',context)


def registerVendor(request):
    if request.method == 'POST':
            form = UserForm(request.POST)
            v_form = VendorForm(request.POST,request.FILES)
            if form.is_valid() and v_form.is_valid:

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user =User.objects.create_user(email=email,first_name=first_name,last_name=last_name,password=password,username=username)
                #user.set_password(password)
                user.role = User.VENDOR
                user.save()

                vendor=v_form.save(commit=False)
                vendor.user=user # vendor linked with (user & user_profile )
                user_profile=UserProfile.objects.get(user=user)
                vendor.user_profile=user_profile
                vendor.save()

                messages.success(request, "YOUR ACCOUNT HAS BEEN REGISTERED SUCCESSFULY..plz wait for vendor approval")
                return redirect('registerVendor')       
            else:
                print("INVALID FORM : ",form.errors)
    else:    
        form = UserForm()
        v_form = VendorForm()

    context={
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html',context)

