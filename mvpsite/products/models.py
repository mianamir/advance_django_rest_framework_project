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


def get_product_by_id(*args, **kwargs):
    try:
        _obj = Product.objects.filter(id=kwargs['product_id']).first()
    except Exception as ex:
        print(f'Exception from Product table, details: {str(ex)}')
        return None
    else:
        if _obj:
            return _obj
    return None


class BuyerPurchase(CustomParentModel):
    purchase_price = models.FloatField(default=0.0, blank=True, null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'BuyerPurchase({self.id}, {self.purchase_price})'

    def __repr__(self):
        return f'BuyerPurchase(id={self.id}, ' \
               f'Name={self.purchase_price})'
