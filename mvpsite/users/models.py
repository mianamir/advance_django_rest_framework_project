from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin
    )

import mvpsite.models


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError(f'Users should have a username.')

        if email is None:
            raise TypeError(f'Users should have a email.')

        # create user
        user = self.model(username=username, email=self.normalize_email(email))

        # save the password
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError(f'Password is required field.')


        # create user
        user = create_user(username, email, password)
        
        # set superuser fields
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, mvpsite.models.CustomParentModel, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'User({self.id}, {self.email}, {username})'

    def __repr__(self):
        return f'User(id={self.id}, email={self.email}, \
        username={username}), is_active={self.is_active}, \
        is_staff={self.is_staff}'
        

