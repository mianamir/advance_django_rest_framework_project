import json

from django.urls import (
    include, 
    path, 
    reverse
    )
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.test import (
    APITestCase, 
    URLPatternsTestCase
    )

from products.models import Product
from products.serializers import ProductSerializer
from users.models import get_user_by_id
from users.constants import (
    ADMIN, 
    SELLER, 
    BUYER
    )


class ProductsListTestCase(APITestCase):

    """ Test module for GET all products API """

    def setUp(self):
        """
        In tests, database is usually recreated from scratch. 
        Add some data in the setUp() method
        """
        # Get User as Seller
        user = get_user_by_id(**{'user_id': 15})

        Product.objects.create(
            product_name="test_product1", 
            amount_available=200.5,
            cost=190.8,
            seller_id=user
            )
        Product.objects.create(
            product_name="test_product2", 
            amount_available=300.5,
            cost=290.8,
            seller_id=user
            )
        Product.objects.create(
            product_name="test_product3", 
            amount_available=400.5,
            cost=390.8,
            seller_id=user
            )

    def test_products(self):
        response = self.client.get('/api/v1/products/')
        print(f'*** list of products({len(response.json())}) *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_single_product(self):
        response = self.client.get('/api/v1/products/1/')
        print(f'*** single product *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_manage_products_with_seller(self):
        """
        To run product management APIs with Seller follow below steps:
        """

        #1 add new user 

        user_data = {
            "password": "123456",
            "username": "test_01",
            "first_name": "test_0001",
            "last_name": "test_00001",
            "email": "test_01@test.com",
            "role": SELLER,
            "deposit": 9000
        }


        user_response = self.client.post('/api/v1/users/create/', user_data)
        print(f'*** added new user *** : {user_response.json()}')
        self.assertEqual(user_response.status_code, HTTP_201_CREATED)

        #2 get the user token
        user_token_resp = self.client.post("/api/v1/login/", 
        {'username': 'test_01', 'password': '123456'})
        print(f'*** user login JWT token *** : {user_token_resp.json()}')
        self.assertEqual(user_token_resp.status_code, HTTP_200_OK)


        #3 add 1st product
        pro1_data = {
        "product_name": "test_product_001",
        "amount_available": 500.5,
        "cost": 590.8
        }

        response = self.client.\
        post('/api/v1/products/create/', 
        pro1_data, HTTP_AUTHORIZATION=f'JWT {user_token_resp.json()["access"]}')
        print(f'*** added 1st product *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        #4 add 2nd product
        pro2_data = {
        "product_name": "test_product_002",
        "amount_available": 5000.5,
        "cost": 6090.8
        }
        
        response = self.client.\
        post('/api/v1/products/create/', 
        pro2_data, HTTP_AUTHORIZATION=f'JWT {user_token_resp.json()["access"]}')
        print(f'*** added 2nd product *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_201_CREATED)


        #4 add 3rd product
        pro3_data = {
        "product_name": "test_product_003",
        "amount_available": 10000.5,
        "cost": 9090.8
        }
        
        response = self.client.\
        post('/api/v1/products/create/', 
        pro3_data, HTTP_AUTHORIZATION=f'JWT {user_token_resp.json()["access"]}')
        print(f'*** added 3rd product *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_201_CREATED)


        #4 update product
        update_pro = {
        "product_name": "updated_test_product_003",
        "amount_available": 10000.5,
        "cost": 9090.8
        }

        # product data
        pro_resp = response.json()['data']
        
        response = self.client.\
        put(f'/api/v1/products/update/{pro_resp["id"]}/', 
        update_pro, 
        HTTP_AUTHORIZATION=f'JWT {user_token_resp.json()["access"]}', follow=True)
        print(f'*** updated product *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_200_OK)


        #5 delete product
        
        response = self.client.\
        delete(f'/api/v1/products/delete/{pro_resp["id"]}/', 
        {}, 
        HTTP_AUTHORIZATION=f'JWT {user_token_resp.json()["access"]}', follow=True)
        print(f'*** deleted product ***')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)


        


