from datetime import datetime as dt
from http import HTTPStatus
import pytest

from fastapi import HTTPException

from app.models import Post
from .fixtures.data import POST_SAVE_DATA

def __info(obj):
    assert obj == '', (f'\ntype = {type(obj)}\nvalue = {obj}')


def __check_exc_info(exc_info, err, msg):
    assert exc_info.value.args[0] == err
    assert exc_info.value.args[1] == msg


def __check_exc_info__not_found(exc_info):
    __check_exc_info(exc_info, HTTPStatus.NOT_FOUND, 'Object(s) not found.')     


def __check(post: Post):
    assert isinstance(post, Post)
    assert post.title == POST_SAVE_DATA['title']
    assert post.content == POST_SAVE_DATA['content']
    assert isinstance(post.created, dt)
    assert post.updated is None
    assert post.likes == 0
    assert post.dislikes == 0


def __get_method(cls, method_name):
    return cls.__getattribute__(method_name)          


@pytest.mark.parametrize('method_name, args, expected_msg', (
    ('has_permission', (None, None), 'has_permission() must be implemented.'),
    ('is_update_allowed', (None, None), 'is_update_allowed() must be implemented.'),
    ('is_delete_allowed', (None,), 'is_delete_allowed() must be implemented.'),
    ('perform_create', (None, None), 'perform_create() must be implemented.'),
    ('perform_update', (None, None), 'perform_update() must be implemented.'),
))
def test_not_implemented_exception(get_crud_base, method_name, args, expected_msg):
    with pytest.raises(NotImplementedError) as exc_info:
        __get_method(get_crud_base, method_name)(*args)
    assert exc_info.value.args[0] == expected_msg


async def test_save(get_crud_base, get_test_session):
    post = await get_crud_base._save(get_test_session, Post(**POST_SAVE_DATA))
    __check(post)


async def test_save_exception(get_crud_base, get_test_session):
    with pytest.raises(HTTPException) as exc_info:
        for _ in range(2): 
            await get_crud_base._save(get_test_session, Post(**POST_SAVE_DATA))
    __check_exc_info(exc_info, HTTPStatus.BAD_REQUEST, 'Object with such a unique values already exists.')     


@pytest.mark.parametrize('method_name', ('get_all_by_attr', 'get_by_attr'))
async def test_not_found_exception(get_crud_base, get_test_session, method_name):
    method = __get_method(get_crud_base, method_name)
    await method(get_test_session, 'title', 'title_value', exception=False)
    with pytest.raises(HTTPException) as exc_info:
        await method(get_test_session, 'title', 'title_value', exception=True)
    __check_exc_info__not_found(exc_info)  

    


@pytest.mark.parametrize('method_name', ('get_all_by_attr', 'get_by_attr'))
async def test_get_by_attr(get_crud_base, get_test_session, method_name):
    method = __get_method(get_crud_base, method_name)
    await get_crud_base._save(get_test_session, Post(**POST_SAVE_DATA))
    result = await method(get_test_session, 'title', POST_SAVE_DATA['title'])
    match method_name:
        case 'get_all_by_attr':
            assert isinstance(result, list)
            __check(result[0])
        case 'get_by_attr':
            __check(result)


async def test_get(get_crud_base, get_test_session):
    method = get_crud_base.get
    post = await method(get_test_session, 1)
    assert post is None
    await get_crud_base._save(get_test_session, Post(**POST_SAVE_DATA))
    post = await method(get_test_session, 1)
    __check(post)


async def test_get_or_404(get_crud_base, get_test_session):
    method = get_crud_base.get_or_404
    with pytest.raises(HTTPException) as exc_info:
        await method(get_test_session, 1)
    __check_exc_info__not_found(exc_info)  
    await get_crud_base._save(get_test_session, Post(**POST_SAVE_DATA))
    post = await method(get_test_session, 1)
    __check(post)


async def test_get_all(get_crud_base, get_test_session):
    method = get_crud_base.get_all
    posts = await method(get_test_session)
    assert posts == []
    with pytest.raises(HTTPException) as exc_info:
        await method(get_test_session, exception=True)
    __check_exc_info__not_found(exc_info)  
    await get_crud_base._save(get_test_session, Post(**POST_SAVE_DATA))
    posts = await method(get_test_session)
    assert isinstance(posts, list)
    __check(posts[0])