from django.urls import path, include
from account import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('account-type', views.AccountTypeViewSet)
router.register('', views.AccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'account'
