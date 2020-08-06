from django.urls import path, include
from account import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('account_type', views.AccountTypeViewSet,
                basename="accounttype")
router.register('', views.AccountViewSet, basename="accounts")

urlpatterns = [
    path('', include((router.urls, 'account'))),
]
