import json

from django.urls import (
    include, 
    path, 
    reverse
    )
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED, HTTP_406_NOT_ACCEPTABLE,
                                   HTTP_403_FORBIDDEN,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.test import (
    APITestCase, 
    URLPatternsTestCase
    )

from products.models import (
    Product, 
    BuyerPurchase, 
    get_product_by_id
    )
from products.serializers import ProductSerializer
from users.constants import (
    AMOUNT_DATA,
    ADMIN, 
    SELLER, 
    BUYER
    )
from users.constants import (
    TEST_NORMAL_USER_EMAIL,
    TEST_SUPER_USER_EMAIL,
    TEST_PASSWORD
)
from users.models import (
    UserProfile, 
    get_user_by_id, 
    get_user_profile_by_id
    )
from users.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer
)
from custom_helpers.custom_responses import (
    get_success_response,
    get_failure_response
)

from custom_helpers.messages import (
    VENDING_MACHINE_COINS_VALID_MESSAGE
)

from custom_helpers.custom_jwt_authentication import CustomJWTAuthentication


class UsersManagementTestCase(APITestCase):

    """ Test module for users APIs """

    def setUp(self):
       ...


    def test_manage_users(self):
        """
        To run users management APIs follow below steps:
        """

        #1 add user 1
        user1_data = {
            "password": "123456",
            "username": "test_user_01",
            "first_name": "test_user_0001",
            "last_name": "test_user_00001",
            "email": "test_user_01@test_user.com",
            "role": SELLER,
            "deposit": 9000
        }

        user_response = self.client.post('/api/v1/users/create/', user1_data)
        print(f'*** added user 1 *** : {user_response.json()}')
        self.assertEqual(user_response.status_code, HTTP_201_CREATED)

        #2 add user 2
        user2_data = {
            "password": "123456",
            "username": "test_user_02",
            "first_name": "test_user_0002",
            "last_name": "test_user_00002",
            "email": "test_user_02@test_user.com",
            "role": SELLER,
            "deposit": 9000
        }

        user_response = self.client.post('/api/v1/users/create/', user2_data)
        print(f'*** added user 2 *** : {user_response.json()}')
        self.assertEqual(user_response.status_code, HTTP_201_CREATED)

        #3 add user 3
        user3_data = {
            "password": "123456",
            "username": "test_user_03",
            "first_name": "test_user_0003",
            "last_name": "test_user_00003",
            "email": "test_user_03@test_user.com",
            "role": BUYER,
            "deposit": 6000
        }

        user_response = self.client.post('/api/v1/users/create/', user3_data)
        print(f'*** added user 3 *** : {user_response.json()}')
        self.assertEqual(user_response.status_code, HTTP_201_CREATED)


        #4 list of users

        response = self.client.get('/api/v1/users/')
        print(f'*** list of users({len(response.json())}) *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_200_OK)

        # single user

        response = self.client.get('/api/v1/users/1/')
        print(f'*** single user *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_200_OK)

        #4 update user
        update_user = {
            "username": "updated_test_user_03",
            "first_name": "updated_testing",
            "last_name": "updated_new",
            "email": "updated_test_user_03@google.com",
            "is_staff": False,
            "is_active": False,
            "password": 123456
        }

        # user data
        user_resp = response.json()
        print(f'user_info: {user_resp}')
        
        response = self.client.\
        put(f'/api/v1/users/{user_resp["id"]}/', update_user, follow=True)
        print(f'*** updated user *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_200_OK)


        #5 delete user
        
        response = self.client.\
        delete(f'/api/v1/users/{user_resp["id"]}/', {}, follow=True)
        print(f'*** deleted user ***')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # ************* DEPOSIT ***********************************************
        #6 deposit api

        # get the user token
        user_token_resp = self.client.post("/api/v1/login/", 
        {'username': 'test_user_03', 'password': '123456'})
        print(f'*** user login JWT token *** : {user_token_resp.json()}')
        self.assertEqual(user_token_resp.status_code, HTTP_200_OK)

        # deposit failure edge case
        deposit_invalid_data = {
            "deposit": 1001
        }
        
        response = self.client.\
        post(f'/api/v1/deposit/', 
        deposit_invalid_data, 
        HTTP_AUTHORIZATION=f'JWT {user_token_resp.json()["access"]}')
        print(f'*** deposit api failure *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_406_NOT_ACCEPTABLE)

        # deposit success case
        deposit_valid_data = {
            "deposit": 100
        }
        
        response = self.client.\
        post(f'/api/v1/deposit/', 
        deposit_valid_data, 
        HTTP_AUTHORIZATION=f'JWT {user_token_resp.json()["access"]}')
        print(f'*** deposit api success *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_200_OK)

        # *************** BUY ************************************************
        #7 buy api

        #7.1 add seller user
        seller_user_data = {
            "password": "123456",
            "username": "test_seller_00001",
            "first_name": "test_seller_first_00001",
            "last_name": "test_seller_last_00002",
            "email": "test_seller_00001@test_seller.com",
            "role": SELLER,
            "deposit": 9000
        }

        user_response = self.client.post('/api/v1/users/create/', seller_user_data)
        print(f'*** added seller user *** : {user_response.json()}')
        self.assertEqual(user_response.status_code, HTTP_201_CREATED)

        seller_user_resp = user_response.json()


         #7.2 get the user token
        user_token_resp = self.client.post("/api/v1/login/", 
        {'username': 'test_seller_00001', 'password': '123456'})
        print(f'*** user login JWT token *** : {user_token_resp.json()}')
        self.assertEqual(user_token_resp.status_code, HTTP_200_OK)


        #7.3 add product for seller user 
        seller_pro_data = {
        "product_name": "test_product_00001",
        "amount_available": 5000.5,
        "cost": 6000.8
        }

        response = self.client.\
        post('/api/v1/products/create/', 
        seller_pro_data, 
        HTTP_AUTHORIZATION=f'JWT {user_token_resp.json()["access"]}')
        print(f'*** added 1st product *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # seller product data
        seller_pro_resp = response.json()['data']

        #7.4 buy failure edge case
        deposit_invalid_data = {
           "product_id": seller_pro_resp['id'],
           "product_amount": 200.5
        }
        
        response = self.client.\
        post(f'/api/v1/buy/', 
        deposit_invalid_data, 
        HTTP_AUTHORIZATION=f'JWT {user_token_resp.json()["access"]}')
        print(f'*** buy api failure *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


        #8 reset vending machine account
        vm_invalid_data = {
           "user": 1
        }
        
        response = self.client.\
        post(f'/api/v1/reset-vending-machine-account/', 
        vm_invalid_data, 
        HTTP_AUTHORIZATION=f'JWT {user_token_resp.json()["access"]}')
        print(f'*** reset vending machine account api failure *** : {response.json()}')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    

        


