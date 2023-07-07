import pytest

from .conftest import Post
from .fixtures.data import POST_SAVE_DATA
from .utils import _info


@pytest.mark.parametrize('attr', (
    'id', 'title', 'content', 'created', 'updated', 'likes', 'dislikes', 'author_id', 'author', '__repr__'
))
def test_model_attr(attr):
    getattr(Post, attr)


def test_model_repr():
    representation = Post(**POST_SAVE_DATA).__repr__()
    assert isinstance(representation, str)
    for attr in ('title', 'content', 'created', 'updated', 'likes', 'dislikes', 'author'):
        assert representation.find(attr) != -1
