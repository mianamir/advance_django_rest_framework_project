from django.db import models
from django.utils import timezone


class CustomParentModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True