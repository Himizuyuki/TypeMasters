from uuid import UUID
from engine_factory import create_engine_default
from post_repository import PostRepository
from sqlalchemy.orm import Session


class PostHandler:
    # create engine on initializzation
    def __init__(self):
        self.db_engine = create_engine_default()

    def add_post_by_user_id(self, post: str, user_id: UUID):
        with Session(self.db_engine) as session:
            post_repository = PostRepository(session)
            post_repository.add_post_by_user_id(post, user_id)


POST_HANDLER = PostHandler()
