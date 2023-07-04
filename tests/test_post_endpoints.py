from .fixtures.data import AUTHOR, ENDPOINT, POST_PAYLOAD
from .fixtures.endpoints_testlib import ( GET,  POST,
                                         get_auth_user_token,
                                         get_headers,
                                         standard_tests)
from .utils import check_created_post, invalid_title_length, json_invalid_values, empty_list


def test_unauthorized_user_can_get_posts():
    standard_tests(GET, ENDPOINT, func_check_valid_response=empty_list)


def test_authorized_user_can_create_post():
    headers=get_headers(get_auth_user_token(AUTHOR))
    standard_tests(POST, ENDPOINT, json=POST_PAYLOAD, headers=headers, func_check_valid_response=check_created_post)


def test_post_json_invalid_values():
    headers=get_headers(get_auth_user_token(AUTHOR))
    json_invalid_values(headers, POST, POST_PAYLOAD)
    invalid_title_length(headers, POST, POST_PAYLOAD)