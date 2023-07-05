from http import HTTPStatus
import pytest

from .fixtures.data import (ENDPOINT, ID, 
                            MY_POSTS_ENDPOINT, 
                            LIKE_ENDPOINT, DISLIKE_ENDPOINT, 
                            AUTH_USER, PUT_PAYLOAD, NO_PERMISSION_MSG, 
                            NO_SELF_LIKE_DISLIKE_MSG, ADMIN, POST_PAYLOAD,
                            POST_NOT_FOUND_MSG, AUTHOR)

from .fixtures.endpoints_testlib import (DELETE, GET, PATCH, POST, PUT,
                                         assert_response,
                                         assert_msg,
                                         get_auth_user_token,
                                         get_headers,
                                         standard_tests)
from .utils import (create_post,
                    check_posts,
                    check_liked_post,
                    check_disliked_post,
                    check_created_post,
                    invalid_title_length,
                    json_invalid_values,
                    check_updated_post)


# === UNAUTHORIZED USER ===
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
))
def test_unauthorized_user_access(method, endpoint, post_id) -> None:
    create_post()
    assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id)


@pytest.mark.parametrize('method, endpoint, path_param', (
    (POST, ENDPOINT, None),
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
    (GET, MY_POSTS_ENDPOINT, None),
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),    
))
def test_unauthorized_user_no_access(method, endpoint, path_param):
    assert_response(HTTPStatus.UNAUTHORIZED, method, endpoint, path_param=path_param)


# === AUTHORIZED USER NOT AUTHOR ===
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (POST, ENDPOINT, None),
    (GET, MY_POSTS_ENDPOINT, None),
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),      
))
def test_authorized_not_author_access(method, endpoint, post_id):
    create_post()
    headers = get_headers(get_auth_user_token(AUTH_USER))
    assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id, headers=headers, json=PUT_PAYLOAD)


@pytest.mark.parametrize('method, endpoint, post_id', (
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
))
def test_authorized_not_author_no_access(method, endpoint, post_id):
    create_post()
    headers = get_headers(get_auth_user_token(AUTH_USER))
    r = assert_response(HTTPStatus.BAD_REQUEST, method, endpoint, path_param=post_id, headers=headers, json=PUT_PAYLOAD)
    assert_msg(r, NO_PERMISSION_MSG)


# === AUTHORIZED USER AUTHOR ===
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (POST, ENDPOINT, None),
    (GET, MY_POSTS_ENDPOINT, None),        
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
))
def test_author_access(method, endpoint, post_id):
    headers = create_post()
    assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id, headers=headers, json=PUT_PAYLOAD)


@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),
))
def test_author_no_access(method, endpoint, post_id):
    headers = create_post()
    r = assert_response(HTTPStatus.BAD_REQUEST, method, endpoint, path_param=post_id, headers=headers)
    assert_msg(r, NO_SELF_LIKE_DISLIKE_MSG)


# === METHODS ===
@pytest.mark.parametrize('not_allowed_methods, endpoint, post_id ', (
    ((PUT, PATCH, DELETE), ENDPOINT, None),
    ((PATCH, POST), ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), LIKE_ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), DISLIKE_ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), MY_POSTS_ENDPOINT, None),
))
def test_not_allowed_methods(not_allowed_methods, endpoint, post_id ):
    for method in not_allowed_methods:
        assert_response(HTTPStatus.METHOD_NOT_ALLOWED, method, endpoint, path_param=post_id)


@pytest.mark.parametrize('user, method, endpoint, post_id, payload, func, msg', (
    (None, GET, ENDPOINT, None, None, check_posts, None),
    (AUTHOR, POST, ENDPOINT, None, POST_PAYLOAD, check_created_post, None),
    (None, GET, ENDPOINT, ID, None, check_created_post, POST_NOT_FOUND_MSG),
    (AUTHOR, PUT, ENDPOINT, ID, PUT_PAYLOAD, check_updated_post, POST_NOT_FOUND_MSG),
    (AUTHOR, DELETE, ENDPOINT, ID, None, check_created_post, POST_NOT_FOUND_MSG),
    (AUTH_USER, GET, LIKE_ENDPOINT, ID, None, check_liked_post, POST_NOT_FOUND_MSG),
    (AUTH_USER, GET, DISLIKE_ENDPOINT, ID, None, check_disliked_post, POST_NOT_FOUND_MSG),
    (AUTHOR, GET, MY_POSTS_ENDPOINT, None, None, check_posts, None),        
))
def test_allowed_methods(user, method, endpoint, post_id, payload, func, msg):
    headers = get_headers(get_auth_user_token(user)) 
    if method is not POST:
        create_post(headers=headers) if user is AUTHOR else create_post()
    json_optional = True if method is PUT else False
    standard_tests(method, endpoint, path_param=post_id, headers=headers, json=payload, json_optional=json_optional, func_check_valid_response=func, msg_invalid_path_param=msg)


# === INVALID PAYLOAD VALUES ===
@pytest.mark.parametrize('method, payload, test_func', (
    (POST, POST_PAYLOAD, json_invalid_values),
    (POST, POST_PAYLOAD, invalid_title_length),
    (PUT, PUT_PAYLOAD, json_invalid_values),
    (PUT, PUT_PAYLOAD, invalid_title_length),
))
def test_json_invalid_values(method, payload, test_func):
    headers = get_headers(get_auth_user_token(AUTHOR)) if method is POST else create_post()
    test_func(method, payload, headers)