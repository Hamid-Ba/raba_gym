from django.db import models
from raba_gym.common.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from .validators import phone_validator



class UserManager(BaseUserManager):
    """User Manager"""

    def create_user(self, phone, password=None, **extra_fields):
        """Custome Create Normal User"""
        if not phone:
            raise ValueError
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """Create Super User"""
        if not phone:
            raise ValueError
        user = self.model(phone=phone, is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.save()

        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    phone = models.CharField(max_length=11, unique=True, validators=[phone_validator])
    full_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.phone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.user} >> {self.bio}"
    