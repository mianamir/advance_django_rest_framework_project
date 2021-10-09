#!/usr/bin/env python

__author__ = "Amir Savvy"
__copyright__ = "Copyright 2021, MVP Vending Machine Project"
__credits__ = ["amir savvy"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Amir Savvy"
__email__ = "mianamirlahore@gmail.com"
__status__ = "Production"



# User info
TEST_NORMAL_USER_EMAIL = f"normal@user.com"
TEST_SUPER_USER_EMAIL = f"super@user.com"
TEST_PASSWORD = f"@#$%123456)(*!@#$"


ADMIN = 1
SELLER = 2
BUYER = 3

AMOUNT_DATA = (5, 10, 20, 50, 100)

UNSAFE_REQUEST_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')

SAFE_REQUEST_METHODS = ('GET', 'HEAD', 'OPTIONS')


EMPTY_RESPONSE = dict()
MESSAGE_KEY = f'message'
DATA_KEY = f'data'
IS_SUCCESSFULL = "is_successfull"
IS_FAILED = "is_failed"