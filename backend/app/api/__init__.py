from fastapi import APIRouter
from app.api import players, scores, songs, plates, spiders, search, segamaid

router = APIRouter()

# 包含各个模块的路由
router.include_router(players.router, prefix="/players", tags=["players"])
router.include_router(scores.router, prefix="/scores", tags=["scores"])
router.include_router(songs.router, prefix="/songs", tags=["songs"])
router.include_router(plates.router, prefix="/plates", tags=["plates"])
router.include_router(spiders.router, prefix="/spiders", tags=["spiders"])
router.include_router(search.router, prefix="/search", tags=["search"])
router.include_router(segamaid.router, prefix="/segamaid", tags=["segamaid"])
