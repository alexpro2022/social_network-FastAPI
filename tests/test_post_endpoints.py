from http import HTTPStatus

from .fixtures.data import AUTH_USER, ENDPOINT, POST_PAYLOAD, INVALID_FIELD_MSG_1, INVALID_FIELD_MSG_2
from .fixtures.endpoints_testlib import (DELETE, GET, PATCH, POST, PUT,
                                         assert_response,
                                         get_auth_user_token,
                                         get_headers,
                                         invalid_methods_test,
                                         standard_tests)
from .utils import check_created_post


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
    empty, space, sequence = '', ' ', 'aaaaaaaaaaaa'
    headers=get_headers(get_auth_user_token(AUTH_USER))
    for key in POST_PAYLOAD:
        invalid_payload = POST_PAYLOAD.copy()
        for invalid_value in ([], (), {}, empty, space, sequence):
            invalid_payload[key] = invalid_value
            response = assert_response(HTTPStatus.UNPROCESSABLE_ENTITY, POST, ENDPOINT, json=invalid_payload, headers=headers)
            if invalid_value in (empty, space):
                assert response.json()['detail'][0]['msg'] == INVALID_FIELD_MSG_1
            if invalid_value == sequence:
                assert response.json()['detail'][0]['msg'] == INVALID_FIELD_MSG_2


def test_post_json_invalid_title_length():
    headers=get_headers(get_auth_user_token(AUTH_USER))
    invalid_payload = POST_PAYLOAD.copy()
    invalid_payload['title'] = 'a' * 100 + 'c'
    assert_response(HTTPStatus.UNPROCESSABLE_ENTITY, POST, ENDPOINT, json=invalid_payload, headers=headers)
