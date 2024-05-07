"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

# noinspection PyUnresolvedReferences
from app.views import *


router = DefaultRouter()
# noinspection PyUnresolvedReferences
router.register('users', UserViewSet, basename='users')
# noinspection PyUnresolvedReferences
router.register('customers', CustomerViewSet, basename='customers')
# noinspection PyUnresolvedReferences
router.register('executors', ExecutorViewSet, basename='executors')
# noinspection PyUnresolvedReferences
router.register('orders', OrderViewSet, basename='orders')
# noinspection PyUnresolvedReferences
router.register('payments', PaymentViewSet, basename='payments')
# noinspection PyUnresolvedReferences
router.register('discusses', DiscussViewSet, basename='discusses')
# noinspection PyUnresolvedReferences
router.register('feedbacks', FeedbackViewSet, basename='feedbacks')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
