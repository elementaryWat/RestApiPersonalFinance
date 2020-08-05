from django.urls import path, include
from account import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('account-type', views.AccountTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),

]

app_name = 'account'
