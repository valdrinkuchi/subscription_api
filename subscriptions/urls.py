from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, SubscriptionViewSet, AccumulatedSubscriptionPriceViewSet

router = DefaultRouter()
router.register(r'v1/customers', CustomerViewSet)
router.register(r'v1/subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/customers/<int:customer_id>/accumulated-price/', AccumulatedSubscriptionPriceViewSet.as_view({'get': 'accumulated_price'}), name='accumulated_price'),
    path('v1/accumulated-price-list/', AccumulatedSubscriptionPriceViewSet.as_view({'get': 'accumulated_prices_list'}), name='accumulated_prices_list'),
]