# from django.db import models

# from django.contrib.auth.models import (
#     AbstractBaseUser, 
#     BaseUserManager, 
#     PermissionsMixin
#     )

# import mvpsite.models

# from .constants import (ADMIN, SELLER, BUYER)


# class UserManager(BaseUserManager):

#     def create_user(self, username, email, deposit=None, role=None, password=None):
#         if username is None:
#             raise TypeError(f'Users should have a username.')

#         if email is None:
#             raise TypeError(f'Users should have a email.')
        
#         email = email.lower()

#         # create user
#         user = self.model(
#             username=username, 
#             email=self.normalize_email(email), 
#             deposit=deposit, 
#             role=role
#             )

#         # save the password
#         user.set_password(password)
#         user.save(using=self._db)
#         return user


#     def create_staffuser(self, email, password):
#         """
#         Creates and saves a staff user with the given email and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password):
#         """
#         Creates and saves a superuser with the given email and password.
#         """
#         user = self.create_user(email,password=password)
#         user.staff = True
#         user.admin = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser, mvpsite.models.CustomParentModel, PermissionsMixin):

#     ROLE_CHOICES = (
#         ('Admin', ADMIN),
#         ('Seller', SELLER),
#         ('Buyer', BUYER)
#     )

#     username = models.CharField(max_length=100, unique=True, db_index=True)
#     email = models.EmailField(max_length=255, unique=True, db_index=True)
#     role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
#     deposit = models.FloatField(blank=True, null=True)
#     active = models.BooleanField(default=True)
#     admin = models.BooleanField(default=False)
#     superuser = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     objects = UserManager()

#     def get_full_name(self):
#         # The user is identified by their email address
#         return self.email

#     def get_short_name(self):
#         # The user is identified by their email address
#         return self.email
    
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True


#     def __str__(self):
#         return f'User({self.id}, {self.email}, {username})'

#     def __repr__(self):
#         return f'User(id={self.id}, email={self.email}, \
#         username={username}), is_active={self.is_active}, \
#         is_staff={self.is_staff}'

#     @property
#     def is_staff(self):
#         return self.admin

#     @property
#     def is_superuser(self):
#         return self.superuser

        

