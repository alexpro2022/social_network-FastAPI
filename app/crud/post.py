from datetime import datetime as dt
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post, User
from app.models.post import Post
from app.schemas import PostCreate, PostUpdate

from .base import CRUDBase


class PostCRUD(CRUDBase[Post, PostCreate, PostUpdate]):
    OBJECT_ALREADY_EXISTS = 'Пост с таким заголовком уже существует.'
    NOT_FOUND = 'Пост(ы) не найден(ы).'
    PERMISSION_DENIED = 'У вас нет права доступа к данному посту.'
    LIKE_DISLIKE_DENIED = 'Запрещено ставить LIKE/DISLIKE собственным постам.'

    def perform_create(self, create_data: dict, user: User) -> None:
        """Adds the author to the post record."""
        if user is not None:
            create_data['author_id'] = user.id

    def perform_update(self, obj: Post, update_data: dict) -> None:
        """Sets the update time."""
        update_data['updated'] = dt.now()

    def has_permission(self, obj: Post, user: User) -> None:
        """Admin or author are only allowed to update/delete the post."""
        if user.is_superuser or user.id == obj.author_id:
            return
        raise HTTPException(HTTPStatus.BAD_REQUEST, self.PERMISSION_DENIED)

    def is_delete_allowed(self, obj: Post) -> None:
        """Always allowed in the project."""
        pass

    def is_update_allowed(self, obj: Post, payload: dict) -> None:
        """Always allowed in the project."""
        pass

    async def get_user_posts(
            self, session: AsyncSession, user: User) -> list[Post] | None:
        return await self.get_all_by_attr(
            session, 'author_id', user.id, exception=True)

    async def like_dislike_post(
        self,
        session: AsyncSession,
        post_id: int,
        user: User,
        like: bool = True,
    ) -> Post | None:
        post: Post = await self.get_or_404(session, post_id)
        if post.author_id == user.id:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, self.LIKE_DISLIKE_DENIED)
        if like:
            post.likes += 1
        else:
            post.dislikes += 1
        return await self._save(session, post)


post_crud = PostCRUD(Post)
