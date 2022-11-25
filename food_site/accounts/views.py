from django.shortcuts import render, redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

#restrict the user and vendor accessing each other's page.
from django.core.exceptions import PermissionDenied

def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):

    if request.user.is_authenticated:
        messages.warning(request, 'You are not logged in')
        return redirect('dashboard')

    elif request.method == 'POST':
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

    if request.user.is_authenticated:
        messages.warning(request, 'You are not logged in')
        return redirect('dashboard')

    elif request.method == 'POST':
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

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are not logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user=auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request,'You are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request,'Invalid email or password')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are now logged out.')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user= request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')

















