from fastapi import APIRouter

from src.api.passengers import router as passengers_router
from src.api.auth import router as auth_router

router = APIRouter(prefix='/api/v1')
router.include_router(passengers_router)
router.include_router(auth_router)
