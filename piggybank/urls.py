"""piggybank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

from core import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.SimpleRouter()
router.register(r'categories', views.CategoryModelViewset, basename="category"),
router.register(r'transactions', views.TransactionModelViewset, basename="transaction")

urlpatterns = [
                  path('login/', obtain_auth_token, name='obtain-auth-token'),
                  path('admin/', admin.site.urls),
                  path('currencies/', views.CurrencyListAPIView.as_view(), name='currencies')

              ] + router.urls
