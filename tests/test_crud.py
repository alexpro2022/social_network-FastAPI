import pytest

from app.models import User


@pytest.mark.parametrize('method, args', (
    ('has_permission', (None, None)),
    ('is_update_allowed', (None, None)),
    ('is_delete_allowed', (None,)),
    ('perform_create', (None, None)),
    ('perform_update', (None, None)),
))
def test_not_implemented(get_crud_base, method, args):
    with pytest.raises(NotImplementedError):
        get_crud_base.__getattribute__(method)(*args)
