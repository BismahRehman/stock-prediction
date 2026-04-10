from fastapi import APIRouter
from fastapi import Depends

from app.schema.prediction import RequestModel,TrainResponse
from app.service.prediction import train_stocks
from app.dependency import get_current_user, get_token, get_db
from app.repository.prediction import prediction_result

router = APIRouter(prefix="/prediction", tags=["Model"])

@router.post("/train",response_model=TrainResponse)
async def train_model(req: RequestModel, current_user: str = Depends(get_current_user), token = Depends(get_token)   , db =Depends(get_db) ):

    accuracy_results = await (train_stocks(req , token, db,current_user))
    model=req.model_name
    await (prediction_result(current_user,accuracy_results,model,db))

    return TrainResponse(
        model_used=model,
        accuracy=accuracy_results
    )


