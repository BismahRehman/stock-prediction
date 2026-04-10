from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends


from app.dependency import get_current_user, get_db

from app.repository.history import user_history
from app.schema.history import ResponseHistory

router = APIRouter(prefix="/prediction history", tags=["Model"])


@router.get("/history", response_model=List[ResponseHistory])
async def history(current_user: str = Depends(get_current_user), db = Depends(get_db)):


    results = await (user_history(db, current_user) )

    return results