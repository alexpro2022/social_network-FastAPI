from datetime import datetime as dt
import pytest

from .conftest import Post, User
from .fixtures.data import POST_SAVE_DATA
from .utils import _info


@pytest.mark.parametrize(
    'attr_name,', ('id', 'title', 'content', 'created', 'updated',
                   'likes', 'dislikes', 'author_id', 'author', '__repr__'))
def test_model_attr(attr_name):
    assert getattr(Post, attr_name, None) is not None



def test_model_repr():
    representation = Post(**POST_SAVE_DATA).__repr__()
    assert isinstance(representation, str)
    for attr in ('title', 'content', 'created', 'updated', 'likes', 'dislikes', 'author'):
        assert representation.find(attr) != -1