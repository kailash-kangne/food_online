from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/',views.vprofile,name='vprofile'),
    path('menu_builder/', views.menu_builder,name='menu_builder'),
    path('menu_builder/category/<int:pk>', views.foodItems_by_category,name='foodItems_by_category'),
    
    #CURD
    path('menu_builder/category/add/', views.add_category ,name='add_category'),
    #path('menu_builder/category/delete/', views.delete_category ,name='delete_category'),
    path('menu_builder/category/edit/<int:pk>', views.edit_category ,name='edit_category'),
     
    
]
