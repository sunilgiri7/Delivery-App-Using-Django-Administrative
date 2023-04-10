"""
URL configuration for deliver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from customer.views import Index, About, Order,OrderConfirmation, OrderPayConfirmation, Menu,MenuSearch
from django.conf import settings
from django.conf.urls.static import static

from customer import views

urlpatterns = [
    path('', views.SignUp, name='signup'),
    path('login', views.LogIn, name='login'),
    path('logout', views.LogOutPage, name='logout'),
    path('home/', views.HomePage, name='home'),

    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('restaurant/', include('restaurant.urls')),
    # path('home/', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),
    path('order/', Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', OrderPayConfirmation.as_view(), name='payment-confirmation'),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)