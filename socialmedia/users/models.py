from django.db import models
from socialmedia.common.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin



class BaseUserManager(BUM):
    def create_user(self, username, is_active=True, is_admin=False, password=None):
        if not username:
            raise ValueError("Users must have an username address")

        user = self.model(username=username, is_active=is_active, is_admin=is_admin)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    username = models.CharField(verbose_name = "username",
                              unique=True, max_length = 255)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    posts_count = models.PositiveIntegerField(default=0)
    subscribers_count = models.PositiveIntegerField(default=0)
    subscriptions_count = models.PositiveIntegerField(default=0)
    bio = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.user} >> {self.bio}"






