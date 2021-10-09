from django.db import models
from django.contrib.auth import get_user_model

from mvpsite.models import CustomParentModel

User = get_user_model()


class Product(CustomParentModel):
    product_name = models.CharField(max_length=50, blank=True, null=True)
    amount_available = models.FloatField(default=0.0, blank=True, null=True)
    cost = models.FloatField(default=0.0, blank=True, null=True)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                  blank=True, null=True)

    def __str__(self):
        return f'Product({self.id}, {self.product_name})'

    def __repr__(self):
        return f'Product(id={self.id}, ' \
               f'Name={self.product_name}, seller={self.user.full_name})'

