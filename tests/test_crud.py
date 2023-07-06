import pytest

def test_not_implemented(get_crud_base):
    with pytest.raises(NotImplementedError):
        get_crud_base.has_permission(None, None)
        get_crud_base.is_update_allowed(None, None)
        get_crud_base.is_delete_allowed(None, None)
        get_crud_base.perform_create(None, None)
        get_crud_base.perform_update(None, None)
