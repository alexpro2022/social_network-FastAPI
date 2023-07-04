from http import HTTPStatus

from .fixtures.data import AUTHOR, AUTH_USER, ENDPOINT, POST_PAYLOAD, PUT_PAYLOAD, POST_NOT_FOUND_MSG, NO_PERMISSION_MSG
from .fixtures.endpoints_testlib import (DELETE, GET, PATCH, POST, PUT,
                                         assert_response,
                                         get_auth_user_token,
                                         get_headers,
                                         not_allowed_methods_test,
                                         standard_tests)
from .utils import check_created_post, check_updated_post, invalid_title_length, json_invalid_values, create_post, check_my_posts

MY_POSTS_ENDPOINT = f'{ENDPOINT}/my_posts'
LIKE_ENDPOINT = f'{ENDPOINT}/like'
DISLIKE_ENDPOINT = f'{ENDPOINT}/dislike'
ID = 1


def test_not_allowed_methods():
    for endpoint, path_param in (
        (MY_POSTS_ENDPOINT, None),
        (LIKE_ENDPOINT, ID),
        (DISLIKE_ENDPOINT, ID),
    ):
        not_allowed_methods_test((DELETE, PATCH, POST, PUT), endpoint, path_param)


def test_unauthorized_user_cannot_get():
    for endpoint, path_param in (
        (MY_POSTS_ENDPOINT, None),
        (LIKE_ENDPOINT, ID),
        (DISLIKE_ENDPOINT, ID),
    ):    
        assert_response(HTTPStatus.UNAUTHORIZED, GET, endpoint, path_param=path_param)


def test_author_can_get_his_posts():
    headers = create_post()
    standard_tests(GET, MY_POSTS_ENDPOINT, headers=headers, func_check_valid_response=check_my_posts)

