from django.urls import path, include
from main.categories import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TransactionCategoryViewSet,
                basename="transaction_category")

urlpatterns = [
    path('', include((router.urls, 'transaction'))),
]
