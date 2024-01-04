from fastapi import APIRouter
from . import users, auth, person, posts, votes

router = APIRouter()

router.include_router(router=users.router, prefix="/users", tags=["Users"])
router.include_router(router=auth.router, prefix="/auth", tags=["Auth"])
router.include_router(router=person.router, prefix="/person", tags=["Person"])
router.include_router(router=posts.router, prefix="/posts", tags=["Posts"])
router.include_router(router=votes.router, prefix="/votes", tags=["Votes"])
