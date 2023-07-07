from datetime import datetime as dt
from http import HTTPStatus
import pytest

from fastapi import HTTPException

from app.models import Post
from .fixtures.data import POST_PAYLOAD, POST_SAVE_DATA

def __info(obj):
    assert obj == '', (f'\ntype = {type(obj)}\nvalue = {obj}')

@pytest.mark.parametrize('method, args, expected_msg', (
    ('has_permission', (None, None), 'has_permission() must be implemented.'),
    ('is_update_allowed', (None, None), 'is_update_allowed() must be implemented.'),
    ('is_delete_allowed', (None,), 'is_delete_allowed() must be implemented.'),
    ('perform_create', (None, None), 'perform_create() must be implemented.'),
    ('perform_update', (None, None), 'perform_update() must be implemented.'),
))
def test_not_implemented_exception(get_crud_base, method, args, expected_msg):
    with pytest.raises(NotImplementedError) as exc_info:
        get_crud_base.__getattribute__(method)(*args)
    assert exc_info.value.args[0] == expected_msg


@pytest.mark.parametrize('method', ('get_all_by_attr', 'get_by_attr'))
async def test_not_found_exception(get_crud_base, get_test_session, method):
    with pytest.raises(HTTPException) as exc_info:
        await get_crud_base.__getattribute__(method)(get_test_session, 'title', 'title_value', True)
    assert exc_info.value.args[0] == HTTPStatus.NOT_FOUND
    assert exc_info.value.args[1] == 'Object(s) not found.'


async def test_save(get_crud_base, get_test_session):
    obj = await get_crud_base._save(get_test_session, Post(**POST_SAVE_DATA))
    assert isinstance(obj, Post)
    assert obj.title == POST_SAVE_DATA['title']
    assert obj.content == POST_SAVE_DATA['content']
    assert isinstance(obj.created, dt)
    assert obj.updated is None
    assert obj.likes == 0
    assert obj.dislikes == 0


async def test_save_exception(get_crud_base, get_test_session):
    with pytest.raises(HTTPException) as exc_info:
        for _ in range(2): 
            await get_crud_base._save(get_test_session, Post(**POST_SAVE_DATA))
    assert exc_info.value.args[0] == HTTPStatus.BAD_REQUEST
    assert exc_info.value.args[1] == 'Object with such a unique values already exists.'        
