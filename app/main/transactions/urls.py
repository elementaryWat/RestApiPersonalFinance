from django.urls import path, include
from .views import TransactionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', TransactionViewSet,
                basename="transactions")

urlpatterns = [
    path('', include((router.urls, 'transactions'))),
]
