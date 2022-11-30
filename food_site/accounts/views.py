from django.shortcuts import render, redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from vendor.models import Vendor
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
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')

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

            #send verification email
            mail_subject='PLZ ACTIVATE ACCOUNT'
            email_template='accounts/emails/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)

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
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')

    elif request.method == 'POST':
            form = UserForm(request.POST)
            v_form = VendorForm(request.POST,request.FILES)
            if form.is_valid() and v_form.is_valid():

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

                #send verification email
                mail_subject='PLZ ACTIVATE ACCOUNT'
                email_template='accounts/emails/account_verification_email.html'
                send_verification_email(request,user,mail_subject,email_template)

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
        messages.warning(request, 'You are already logged in')
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


def activate(request,uidb64,token):
    #activate the user by setting the is_active status to True
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"congratultions! your account is activate.")
        return redirect('myAccount')
    else:
        messages.error(request,"Invalid activation link/token")
        return redirect('myAccount')

def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']

        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            
            #send reset_password email
            mail_subject='Reset your password'
            email_template='accounts/emails/reset_password_email.html'

            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,"reset password link sent to email")
            return redirect('login')
        else:
            messages.error(request," account does not exist")
            return redirect('forgot_password')


    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    #validate user by decoding
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,"plz reset your password")
        return redirect('reset_password')
    else:
        messages.error(request,"Invalid reset link/token")
        redirect('myAccount')

def reset_password(request):
    if request.method=='POST':
        password = request.POST['password']
        confirm_password= request.POST['confirm_password']

        if password == confirm_password:
            pk= request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,"Your password has been reset successfully")
            return redirect('login')
        else:
            messages.error(request,"Passwords do not match")
            return redirect('reset_password')

    return render(request,'accounts/reset_password.html')











# import sys
# import json 
# from django.utils.html import escape
# def checkrequest(request):
#     # print("REQ :",request)
#     # print(request.__dict__, file=sys.stderr)
#     dictionary=[request.__dict__]
    
#     return HttpResponse(dictionary)
#     #return HttpResponse(escape(repr(request)))

    




   












