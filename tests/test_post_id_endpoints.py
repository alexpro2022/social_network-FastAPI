from http import HTTPStatus

from .fixtures.data import AUTH_USER, ENDPOINT, POST_PAYLOAD, PUT_PAYLOAD, NOT_FOUND_MSG, INVALID_FIELD_MSG_1, INVALID_FIELD_MSG_2
from .fixtures.endpoints_testlib import (DELETE, GET, PATCH, POST, PUT,
                                         assert_response,
                                         client,
                                         get_auth_user_token,
                                         get_headers,
                                         invalid_methods_test,
                                         valid_values_standard_tests)
from .utils import check_created_post, check_updated_post

ID = 1


def create_post():
    headers = get_headers(get_auth_user_token(AUTH_USER))
    client.post(ENDPOINT, headers=headers, json=POST_PAYLOAD)
    return headers 


def test_invalid_methods():
    invalid_methods_test((PATCH, POST), ENDPOINT, ID)


def test_unauthorized_user_can_get_post():
    create_post()
    valid_values_standard_tests(
        GET, ENDPOINT, path_param=ID, func_check_valid_response=check_created_post, msg_invalid_path_param=NOT_FOUND_MSG)


def test_unauthorized_user_cannot_put_delete():
    assert_response(HTTPStatus.UNAUTHORIZED, PUT, ENDPOINT, path_param=ID, json=POST_PAYLOAD)
    assert_response(HTTPStatus.UNAUTHORIZED, DELETE, ENDPOINT, path_param=ID)


def test_author_can_put():
    headers = create_post()
    valid_values_standard_tests(PUT, ENDPOINT, path_param=ID, headers=headers, json=PUT_PAYLOAD, json_optional=True, func_check_valid_response=check_updated_post)


def test_author_can_delete():
    headers = create_post()
    valid_values_standard_tests(DELETE, ENDPOINT, path_param=ID, headers=headers, json=PUT_PAYLOAD, json_optional=True, func_check_valid_response=check_created_post)


def test_put_json_invalid_values():
    empty, space, sequence = '', ' ', 'aaaaaaaaaaaa'
    headers = create_post()
    for key in PUT_PAYLOAD:
        invalid_payload = PUT_PAYLOAD.copy()
        for invalid_value in ([], (), {}, empty, space, sequence):
            invalid_payload[key] = invalid_value
            response = assert_response(HTTPStatus.UNPROCESSABLE_ENTITY, PUT, ENDPOINT, path_param=ID, json=invalid_payload, headers=headers)
            if invalid_value in (empty, space):
                assert response.json()['detail'][0]['msg'] == INVALID_FIELD_MSG_1
            if invalid_value == sequence:
                assert response.json()['detail'][0]['msg'] == INVALID_FIELD_MSG_2


def test_post_json_invalid_title_length():
    headers = create_post()
    invalid_payload = PUT_PAYLOAD.copy()
    invalid_payload['title'] = 'a' * 100 + 'c'
    assert_response(HTTPStatus.UNPROCESSABLE_ENTITY, PUT, ENDPOINT, path_param=ID, json=invalid_payload, headers=headers)
