import pytest
import re

from fastapi import HTTPException

from app.models import User


@pytest.mark.parametrize('method, args, msg', (
    ('has_permission', (None, None), 'has_permission() must be implemented.'),
    ('is_update_allowed', (None, None), 'is_update_allowed() must be implemented.'),
    ('is_delete_allowed', (None,), 'is_delete_allowed() must be implemented.'),
    ('perform_create', (None, None), 'perform_create() must be implemented.'),
    ('perform_update', (None, None), 'perform_update() must be implemented.'),
))
def test_not_implemented_exception(get_crud_base, method, args, msg):
    with pytest.raises(NotImplementedError, match=re.escape(msg)):
        get_crud_base.__getattribute__(method)(*args)


@pytest.mark.parametrize('method', ('get_all_by_attr', 'get_by_attr'))
async def test_not_found_exception(get_crud_base, get_test_session, method):
    with pytest.raises(HTTPException, match=re.escape('Object(s) not found.')):
        await get_crud_base.__getattribute__(method)(get_test_session, 'title', None, True)
