from .fixtures.data import AUTH_USER, POST_PAYLOAD, PUT_PAYLOAD


def check_post(response_json: dict, payload: dict, user: dict, updated: bool = False) -> str:
    assert isinstance(response_json['id'], int)
    assert response_json['created'] is not None
    if updated:
        assert response_json['updated'] is not None
    else:
        assert response_json.get('updated') is None
    assert response_json['likes'] == 0
    assert response_json['dislikes'] == 0
    assert response_json['title'] == payload['title']
    assert response_json['content'] == payload['content']
    author = response_json['author']
    assert isinstance(author, dict)
    assert isinstance(author['id'], int)
    assert author['email'] == user['email']
    assert author['is_active'] == True
    assert author['is_superuser'] == False
    assert author['is_verified'] == False        
    return 'DONE'


def check_created_post(response_json: dict):
    return check_post(response_json, POST_PAYLOAD, AUTH_USER)


def check_updated_post(response_json: dict):
    return check_post(response_json, PUT_PAYLOAD, AUTH_USER, updated=True)