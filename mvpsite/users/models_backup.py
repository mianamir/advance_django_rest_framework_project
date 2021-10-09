import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from mvpsite.models import CustomParentModel

User = get_user_model()

from .constants import (ADMIN, SELLER, BUYER)

# from django.utils import timezone
#
# from .managers import CustomUserManager
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     # These fields tie to the roles!
#     ADMIN = 1
#     SELLER = 2
#     BUYER = 3
#
#     ROLE_CHOICES = (
#         (ADMIN, 'Admin'),
#         (SELLER, 'Seller'),
#         (BUYER, 'Buyer')
#     )
#
#     uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='User UUID')
#     # username = models.CharField(max_length=100, blank=False, unique=True)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     is_deleted = models.BooleanField(default=False)
#     created_date = models.DateTimeField(default=timezone.now)
#     modified_date = models.DateTimeField(default=timezone.now)
#     created_by = models.EmailField()
#     modified_by = models.EmailField()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = CustomUserManager()
#
#     def get_full_name(self):
#         """
#         Return the first_name plus the last_name, with a space in between
#         """
#         full_name = f'{self.first_name} {self.last_name}'
#         return full_name.strip()
#
#     def get_short_name(self):
#         """
#         Return the short name for the user
#         """
#         return f'{self.first_name}'
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         return self.is_staff
#
#     @property
#     def is_admin(self):
#         "Is the user a admin member?"
#         if self.role == 1:
#             return True
#         return False
#
#     def __str__(self):
#         return f'User({self.id}, {self.email})'
#
#     def __repr__(self):
#         return f'User(id={self.id}, ' \
#                f'Email={self.email}, ' \
#                f'UID={self.uid})'
#     # class Meta:
#     #     verbose_name = 'users'
#     #     verbose_name_plural = 'users'
#     #     # abstract = False


class UserProfile(CustomParentModel):
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (SELLER, 'Seller'),
        (BUYER, 'Buyer')
    )
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(
      choices=ROLE_CHOICES,
      blank=True,
      null=True,
      default=SELLER
    )

    def __str__(self):
        return f'User Profile({self.id}, {self.role})'

    def __repr__(self):
        return f'User Profile(id={self.id}, ' \
               f'Role={self.role})'

    @property
    def user_role(self):
        "Is the user a member of staff?"
        return self.role


    @property
    def full_name(self):
        """
        Return the first_name plus the last_name, with a space in between
        """
        full_name = f'{self.user.first_name} {self.user.last_name}'
        return full_name.strip()

    @property
    def short_name(self):
        """
        Return the short name for the user
        """
        return f'{self.user.first_name}'

#
# @receiver(post_save, sender=User)
# def add_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)


def get_user_by_id(*args, **kwargs):
    try:
        _obj = User.objects.filter(id=kwargs['id'], userprofile__role=SELLER).first()
    except Exception as ex:
        print(f'Exception from User table, details: {ex}')
        return None
    else:
        if _obj:
            return _obj
    return None