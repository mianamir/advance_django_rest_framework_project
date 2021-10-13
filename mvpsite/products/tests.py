from django.test import TestCase

from django.contrib.auth import get_user_model
from django.test import TestCase

from products.models import Product



class ProductsManagersTests(TestCase):

    def test_product_user(self):
        
        data = {
        "product_name": "new326 testing t-shirt",
        "amount_available": 200.5,
        "cost": 190.8,
        "seller_id": 15
    }

        obj = Product.objects.create(**data)
        
        try:
           ...
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            ...
        with self.assertRaises(TypeError):
            ...
        with self.assertRaises(ValueError):
            ...

    