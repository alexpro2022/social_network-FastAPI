from http import HTTPStatus

from .fixtures.data import AUTH_USER, ENDPOINT, POST_PAYLOAD
from .fixtures.endpoints_testlib import (DELETE, GET, PATCH, POST, PUT,
                                         assert_response,
                                         client,
                                         get_auth_user_token,
                                         get_headers,
                                         invalid_methods_test,
                                         valid_values_standard_tests)
from .utils import check_created_post

ID = 1


def create_post():
    headers = get_headers(get_auth_user_token(AUTH_USER))
    client.post(ENDPOINT, headers=headers, json=POST_PAYLOAD)    


def test_invalid_methods():
    invalid_methods_test((PATCH, POST), ENDPOINT, ID)


def test_unauthorized_user_can_get_post():
    create_post()
    valid_values_standard_tests(GET, ENDPOINT, path_param=ID, func_check_valid_response=check_created_post)


def test_unauthorized_user_cannot_put_delete():
    assert_response(HTTPStatus.UNAUTHORIZED, PUT, ENDPOINT, path_param=ID, json=POST_PAYLOAD)
    assert_response(HTTPStatus.UNAUTHORIZED, DELETE, ENDPOINT, path_param=ID)
