"""ashion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path

from main.views import (
    HomeView,
    CheckoutView,
    ContactView,
    ProductDetailView,
    ShopCartView,
    ShopView,
    RemoveFromCart,
    AddToCart,
    SetAmount,
    PrivacyPolicyView,
)

handler404 = 'main.views.error_404'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('<str:category>/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', ShopCartView.as_view(), name='cart'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('cart/del/<int:pk>/', RemoveFromCart.as_view(), name='remove-from-cart'),
    path('cart/add/<int:pk>', AddToCart.as_view(), name='add-to-cart'),
    path('set-amount/', SetAmount.as_view(), name='set-amount'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)