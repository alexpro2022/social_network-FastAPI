from http import HTTPStatus

from .fixtures.endpoints_testlib import (DELETE, GET, PATCH, POST, PUT,
                                         assert_response,
                                         get_auth_user_token,
                                         get_headers,
                                         invalid_methods_test,
                                         valid_values_standard_tests)

ENDPOINT = 'post'
AUTH_USER = {"email": "testuser@example.com", "password": "testpass"}
POST_PAYLOAD = {
  "title": "POST New post title.",
  "content": "POST New post content."
}


def test_unauthorized_user_can_get_posts():
    def empty_list(response: list) -> str:
        assert response == []
        return 'DONE'    
    valid_values_standard_tests(GET, ENDPOINT, func_check_valid_response=empty_list)


def test_invalid_methods():
    invalid_methods_test((PUT, PATCH, DELETE), ENDPOINT)


def test_unauthorized_user_cannot_create_post():
    assert_response(HTTPStatus.UNAUTHORIZED, POST, ENDPOINT, json=POST_PAYLOAD)


def test_authorized_user_can_create_post():
    def created_post(response_json: dict) -> str:
        assert isinstance(response_json['id'], int)
        assert response_json['created'] is not None
        assert response_json.get('updated') is None
        assert response_json['likes'] == 0
        assert response_json['dislikes'] == 0
        assert response_json['title'] == POST_PAYLOAD['title']
        assert response_json['content'] == POST_PAYLOAD['content']
        author = response_json['author']
        assert isinstance(author, dict)
        assert isinstance(author['id'], int)
        assert author['email'] == AUTH_USER['email']
        assert author['is_active'] == True
        assert author['is_superuser'] == False
        assert author['is_verified'] == False        
        return 'DONE'
    
    headers=get_headers(get_auth_user_token(AUTH_USER))
    valid_values_standard_tests(POST, ENDPOINT, json=POST_PAYLOAD, headers=headers, func_check_valid_response=created_post)


def test_post_json_invalid_values():
    headers=get_headers(get_auth_user_token(AUTH_USER))
    for key in POST_PAYLOAD:
        invalid_payload = POST_PAYLOAD.copy()
        for invalid_value in ([], (), {}):
            invalid_payload[key] = invalid_value
            assert_response(HTTPStatus.UNPROCESSABLE_ENTITY, POST, ENDPOINT, json=invalid_payload, headers=headers)


'''def cargo_post_payload_invalid_zip_value():
    msg = 'Локация не найдена - неверный location_id или zip-код.'
    for invalid_zip in ('12345',):
        for key in ('delivery_zip', 'current_zip'):
            invalid_payload = POST_PAYLOAD.copy()
            invalid_payload[key] = invalid_zip
            response = assert_response(HTTPStatus.NOT_FOUND, POST, ENDPOINT, payload=invalid_payload)
            assert response.json() == {'detail': msg}, response.json()


def cargo_post_payload_invalid_zip_length():
    for invalid_zip in ('', ' ', '1234', '123456'):
        for key in ('delivery_zip', 'current_zip'):
            invalid_payload = POST_PAYLOAD.copy()
            invalid_payload[key] = invalid_zip
            assert_response(HTTPStatus.UNPROCESSABLE_ENTITY, POST, ENDPOINT, payload=invalid_payload)
'''