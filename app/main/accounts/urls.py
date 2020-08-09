from django.urls import path, include
from main.accounts import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('account_type', views.AccountTypeViewSet,
                basename="accounttype")
router.register('', views.AccountViewSet, basename="accounts")

urlpatterns = [
    path('', include((router.urls, 'accounts'))),
]
