from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


"""
While defining a custom user admin in app's admin.py, 
First unregister the default User model admin before registering your own.
"""
# admin.site.unregister(User)
#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['id',
#                     'first_name',
#                     'last_name',
#                     'email',
#                     'is_staff',
#                     'is_superuser',
#                     'is_active'
#                     ]