from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from encrypted_id.models import EncryptedIDModel, EncryptedIDManager

# Create your models here.

# Customized User model


class UserManager(BaseUserManager, EncryptedIDManager):
    def create_user(self, email, password=None):
        """
        Create and save a User with the given email and password
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with given email and password.
        """
        user = self.create_user(email, password=password)
        user.staff = True
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password
        """
        user = self.create_user(email, password=password)
        user.staff = True
        user.admin = True
        user.save()
        return user

    def get_by_natural_key(self, value):
        return self.get(**{self.model.USERNAME_FIELD: value})


class User(AbstractBaseUser, EncryptedIDModel):
    first_name = models.CharField(max_length=100, blank=True, default="")
    last_name = models.CharField(max_length=100, blank=True, default="")
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(
        default=True,
        help_text="""
            Designates whether this user should be treated as active.
            Un-select this instead deleting accounts.
        """
    )
    staff = models.BooleanField(
        default=False,
        help_text="""
            People from company
        """
    )
    admin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email and password are required default
    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does User have a specific permission"""
        return True

    def has_module_perms(self, app_label):
        """Does user have permission to view the app `app_label`?"""
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
