from http import HTTPStatus

from .fixtures.data import AUTH_USER, ENDPOINT, POST_PAYLOAD, INVALID_FIELD_MSG_1, INVALID_FIELD_MSG_2
from .fixtures.endpoints_testlib import (DELETE, GET, PATCH, POST, PUT,
                                         assert_response,
                                         get_auth_user_token,
                                         get_headers,
                                         invalid_methods_test,
                                         standard_tests)
from .utils import check_created_post, invalid_title_length, json_invalid_values


def test_unauthorized_user_can_get_posts():
    def empty_list(response_json: list) -> str:
        assert response_json == []
        return 'DONE'
    
    standard_tests(GET, ENDPOINT, func_check_valid_response=empty_list)


def test_invalid_methods():
    invalid_methods_test((PUT, PATCH, DELETE), ENDPOINT)


def test_unauthorized_user_cannot_create_post():
    assert_response(HTTPStatus.UNAUTHORIZED, POST, ENDPOINT, json=POST_PAYLOAD)


def test_authorized_user_can_create_post():
    headers=get_headers(get_auth_user_token(AUTH_USER))
    standard_tests(POST, ENDPOINT, json=POST_PAYLOAD, headers=headers, func_check_valid_response=check_created_post)


def test_post_json_invalid_values():
    headers=get_headers(get_auth_user_token(AUTH_USER))
    json_invalid_values(headers, POST, POST_PAYLOAD)
    invalid_title_length(headers, POST, POST_PAYLOAD)


'''def test_post_json_invalid_title_length():
    headers=get_headers(get_auth_user_token(AUTH_USER))
    invalid_title_length(headers, POST, POST_PAYLOAD)'''

