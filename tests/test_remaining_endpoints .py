from http import HTTPStatus
import pytest

from .fixtures.data import ADMIN, AUTH_USER, ENDPOINT, NO_SELF_LIKE_DISLIKE_MSG, POST_NOT_FOUND_MSG, POST_PAYLOAD, PUT_PAYLOAD, NO_PERMISSION_MSG
from .fixtures.endpoints_testlib import (DELETE, GET, PATCH, POST, PUT,
                                         assert_response,
                                         assert_msg,
                                         get_auth_user_token,
                                         get_headers,
                                         not_allowed_methods_test,
                                         standard_tests)
from .utils import (create_post,
                    check_posts,
                    check_liked_post,
                    check_disliked_post,
                    empty_list,
                    check_created_post,
                    check_post,
                    check_updated_post)

MY_POSTS_ENDPOINT = f'{ENDPOINT}/my_posts'
LIKE_ENDPOINT = f'{ENDPOINT}/like'
DISLIKE_ENDPOINT = f'{ENDPOINT}/dislike'
ID = 1


# === UNAUTHORIZED USER ===
@pytest.mark.parametrize('case', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
))
def test_unauthorized_user_access(case: tuple) -> None:
    create_post()
    method, endpoint, post_id = case
    assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id)


@pytest.mark.parametrize('case', (
    (POST, ENDPOINT, None),
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
    (GET, MY_POSTS_ENDPOINT, None),
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),    
))
def test_unauthorized_user_no_access(case: tuple):
    method, endpoint, path_param = case
    assert_response(HTTPStatus.UNAUTHORIZED, method, endpoint, path_param=path_param)


# === AUTHORIZED USER NOT AUTHOR ===
@pytest.mark.parametrize('case', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (POST, ENDPOINT, None),
    (GET, MY_POSTS_ENDPOINT, None),
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),      
))
def test_authorized_not_author_access(case: tuple):
    create_post()
    headers = get_headers(get_auth_user_token(AUTH_USER))
    method, endpoint, post_id = case
    assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id, headers=headers, json=PUT_PAYLOAD)


@pytest.mark.parametrize('case', (
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
))
def test_authorized_not_author_no_access(case: tuple):
    create_post()
    headers = get_headers(get_auth_user_token(AUTH_USER))
    method, endpoint, post_id = case
    r = assert_response(HTTPStatus.BAD_REQUEST, method, endpoint, path_param=post_id, headers=headers, json=PUT_PAYLOAD)
    assert_msg(r, NO_PERMISSION_MSG)


# === AUTHORIZED USER AUTHOR ===
@pytest.mark.parametrize('case', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (POST, ENDPOINT, None),
    (GET, MY_POSTS_ENDPOINT, None),        
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
))
def test_author_access(case: tuple):
    headers = create_post()
    method, endpoint, post_id = case
    assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id, headers=headers, json=PUT_PAYLOAD)


@pytest.mark.parametrize('case', (
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),
))
def test_author_no_access(case: tuple):
    headers = create_post()
    method, endpoint, post_id = case
    r = assert_response(HTTPStatus.BAD_REQUEST, method, endpoint, path_param=post_id, headers=headers)
    assert_msg(r, NO_SELF_LIKE_DISLIKE_MSG)


# === AUTHORIZED USER ADMIN ===
@pytest.mark.parametrize('case', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (POST, ENDPOINT, None),
    (GET, MY_POSTS_ENDPOINT, None),        
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),    
))
def test_author_access(case: tuple):
    create_post()
    headers = get_headers(get_auth_user_token(ADMIN))
    method, endpoint, post_id = case
    assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id, headers=headers, json=PUT_PAYLOAD)


# === METHODS ===
@pytest.mark.parametrize('case', (
    ((PUT, PATCH, DELETE), ENDPOINT, None),
    ((PATCH, POST), ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), LIKE_ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), DISLIKE_ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), MY_POSTS_ENDPOINT, None),
))
def test_not_allowed_methods(case: tuple):
    not_allowed_methods, endpoint, post_id = case
    for method in not_allowed_methods:
        assert_response(HTTPStatus.METHOD_NOT_ALLOWED, method, endpoint, path_param=post_id)

