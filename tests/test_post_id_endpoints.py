from http import HTTPStatus
import pytest

from .fixtures.data import AUTH_USER, ENDPOINT, POST_PAYLOAD, PUT_PAYLOAD, POST_NOT_FOUND_MSG, NO_PERMISSION_MSG
from .fixtures.endpoints_testlib import (DELETE, GET, PATCH, POST, PUT,
                                         assert_response,
                                         get_auth_user_token,
                                         get_headers,
                                         not_allowed_methods_test,
                                         standard_tests)
from .utils import check_created_post, check_updated_post, invalid_title_length, json_invalid_values, create_post

ID = 1


def test_not_allowed_methods():
    not_allowed_methods_test((PATCH, POST), ENDPOINT, ID)


def test_unauthorized_user_can_get_post():
    create_post()
    standard_tests(
        GET, ENDPOINT, path_param=ID, func_check_valid_response=check_created_post, msg_invalid_path_param=POST_NOT_FOUND_MSG)


@pytest.mark.parametrize('method', (PUT, DELETE))
def test_unauthorized_user_cannot_put_delete_post(method: str):
    assert_response(HTTPStatus.UNAUTHORIZED, method, ENDPOINT, path_param=ID, json=POST_PAYLOAD)


@pytest.mark.parametrize('method', (PUT, DELETE))
def test_authorized_cannot_put_delete_post(method: str):
    create_post()
    headers = get_headers(get_auth_user_token(AUTH_USER))
    response = assert_response(HTTPStatus.BAD_REQUEST, method, ENDPOINT, path_param=ID, headers=headers, json=PUT_PAYLOAD)
    assert response.json()['detail'] == NO_PERMISSION_MSG


@pytest.mark.parametrize('case', (
    (PUT, check_updated_post),
    (DELETE, check_created_post),
))
def test_author_can_put_delete_post(case: tuple):
    headers = create_post()
    method, check_func = case
    standard_tests(method, ENDPOINT, path_param=ID, headers=headers, json=PUT_PAYLOAD, json_optional=True, func_check_valid_response=check_func)


def test_author_put_json_invalid_values():
    headers = create_post()
    json_invalid_values(headers, PUT, PUT_PAYLOAD)
    invalid_title_length(headers, PUT, PUT_PAYLOAD)
    

