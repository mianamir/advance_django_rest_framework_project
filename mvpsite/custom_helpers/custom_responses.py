#!/usr/bin/env python

"""
Provides custom response data.
"""
from users.constants import (
    EMPTY_RESPONSE,
    MESSAGE_KEY,
    DATA_KEY,
    IS_SUCCESSFULL,
    IS_FAILED
)
from custom_helpers.messages import (
    SUCCESSFULL_RESPONSE_MESSAGE,
    FAILED_RESPONSE_MESSAGE
)


def get_success_response(*args, **kwargs):
    res = {
        DATA_KEY: kwargs['data'],
        IS_SUCCESSFULL: True,
        IS_FAILED: False,
        MESSAGE_KEY: SUCCESSFULL_RESPONSE_MESSAGE
    }
    return res


def get_failure_response(*args, **kwargs):
    res = {
        DATA_KEY: EMPTY_RESPONSE,
        IS_SUCCESSFULL: False,
        IS_FAILED: True,
        MESSAGE_KEY: FAILED_RESPONSE_MESSAGE
    }
    return res