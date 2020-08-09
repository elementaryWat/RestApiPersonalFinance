from django.db import models
from enum import Enum
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Creates and saves a new user
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Custom user model that supports using email instead of username
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = "email"


class AccountType(models.Model):
    # Model for defining the Transactions Account Type e.g Wallet, Savings
    name = models.CharField(max_length=50, unique=True)
    icon_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    # Model for creating a user's transactions account
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=512)
    account_type = models.ForeignKey(
        AccountType,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class TransactionCategory(models.Model):
    # Model for creating a transacion Category
    name = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=50, blank=True)
    CATEGORY_TYPE_CHOICES = [
        ('EX', _('Expense')),
        ('IN', _('Income')),
    ]
    category_type = models.CharField(
        max_length=5,
        choices=CATEGORY_TYPE_CHOICES
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
