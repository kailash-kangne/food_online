
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as MarketplaceViews
from orders import views as OrdersViews

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.index,name='home'),
    path('', include('accounts.urls')),
    path('marketplace/',include('marketplace.urls')),
    # path('orders/', include('orders.urls')),
    
    #cart
    #path('cart/',MarketplaceViews.cart,name='cart'),
    #path('search/',MarketplaceViews.search,name='search'),
    #path('checkout/',MarketplaceViews.checkout,name='checkout'),
    path('place_order/',OrdersViews.place_order,name='place_order'),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
