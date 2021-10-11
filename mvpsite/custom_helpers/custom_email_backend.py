"""
Provides a set of pluggable authentication policies.
"""

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EmailAuthBackend(object):
    ''' Custom authentication backend.  Allows users to login using their email address '''

    def authenticate(self, email=None, password = None):
        ''' the main method of the backend '''

        try:
            user = User.objects.get(email = email)

            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk = user_id) # Note that you MUST use pk = user_id in getting the user.  Otherwise, it will fail and even though the user is authenticated, the user will not be logged in

            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
            

class CustomEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | 
                Q(email__iexact=username)).distinct()
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except UserModel.MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None