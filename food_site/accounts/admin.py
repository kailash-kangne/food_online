from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

#make password non-editable
class CustomUserAdmin(UserAdmin):
    list_display =('email', 'username', 'role','is_active')
    ordering = ("-date_joined",) # - : descending order
    filter_horizontal = ()
    fieldsets = ()
    list_filter =  ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)