from .fixtures.data import AUTH_USER, POST_PAYLOAD


def check_created_post(response_json: dict) -> str:
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