from http import HTTPStatus
import pytest

from fastapi import HTTPException


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
    expected_msg = 'Object(s) not found.'
    with pytest.raises(HTTPException) as exc_info:
        await get_crud_base.__getattribute__(method)(get_test_session, 'title', None, True)
    assert exc_info.value.args[0] == HTTPStatus.NOT_FOUND
    assert exc_info.value.args[1] == expected_msg