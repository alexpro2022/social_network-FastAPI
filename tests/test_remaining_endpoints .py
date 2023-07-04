from http import HTTPStatus
import pytest

from .fixtures.data import AUTHOR, AUTH_USER, ENDPOINT, NO_SELF_LIKE_DISLIKE_MSG
from .fixtures.endpoints_testlib import (DELETE, GET, PATCH, POST, PUT,
                                         assert_response,
                                         assert_msg,
                                         get_auth_user_token,
                                         get_headers,
                                         not_allowed_methods_test,
                                         standard_tests)
from .utils import create_post, check_my_posts, check_liked_post, check_disliked_post, empty_list

MY_POSTS_ENDPOINT = f'{ENDPOINT}/my_posts'
LIKE_ENDPOINT = f'{ENDPOINT}/like'
DISLIKE_ENDPOINT = f'{ENDPOINT}/dislike'
ID = 1


@pytest.mark.parametrize('case', (
    (MY_POSTS_ENDPOINT, None),
    (LIKE_ENDPOINT, ID),
    (DISLIKE_ENDPOINT, ID),        
))
def test_not_allowed_methods(case: tuple):
    endpoint, path_param = case
    not_allowed_methods_test((DELETE, PATCH, POST, PUT), endpoint, path_param)


@pytest.mark.parametrize('case', (
    (MY_POSTS_ENDPOINT, None),
    (LIKE_ENDPOINT, ID),
    (DISLIKE_ENDPOINT, ID),    
))
def test_unauthorized_user_cannot_get(case: tuple):
    endpoint, path_param = case
    assert_response(HTTPStatus.UNAUTHORIZED, GET, endpoint, path_param=path_param)


def test_author_can_get_his_posts():
    headers = create_post()
    standard_tests(GET, MY_POSTS_ENDPOINT, headers=headers, func_check_valid_response=check_my_posts)


def test_authorized_get_empty_list():
    create_post()
    headers=get_headers(get_auth_user_token(AUTH_USER))
    standard_tests(GET, MY_POSTS_ENDPOINT, headers=headers, func_check_valid_response=empty_list)


@pytest.mark.parametrize('endpoint', (LIKE_ENDPOINT, DISLIKE_ENDPOINT))
def test_author_cannot_like_dislike_his_post(endpoint: str):
    headers = create_post()
    r = assert_response(HTTPStatus.BAD_REQUEST, GET, endpoint, path_param=ID, headers=headers)
    assert_msg(r, NO_SELF_LIKE_DISLIKE_MSG)


@pytest.mark.parametrize('case', (
    (LIKE_ENDPOINT, check_liked_post),
    (DISLIKE_ENDPOINT, check_disliked_post),
))
def test_authorized_can_like_dislike_post(case: tuple):
    create_post()
    headers = get_headers(get_auth_user_token(AUTH_USER))
    endpoint, check_func = case
    r = assert_response(HTTPStatus.OK, GET, endpoint, path_param=ID, headers=headers)
    check_func(r.json())
