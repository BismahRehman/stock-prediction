from fastapi import APIRouter, Depends

from app.schema.prediction import RequestModel, TrainResponse
from app.service.prediction import train_stocks
from app.dependency import get_current_user, get_token, get_db
from app.repository.prediction import prediction_result

router = APIRouter(prefix="/prediction", tags=["Model"])


# -----------------------------------------
# TRAIN MODEL ENDPOINT
# -----------------------------------------
@router.post("/train", response_model=TrainResponse)
async def train_model(
    req: RequestModel,
    current_user: str = Depends(get_current_user),
    token=Depends(get_token),
    db=Depends(get_db)
):

    # Train ML model and get accuracy
    accuracy_results = await train_stocks(req, token, db, current_user)

    model = req.model_name

    # Store training result in history table
    await prediction_result(current_user, accuracy_results, model, db)

    # Return response to client
    return TrainResponse(
        model_used=model,
        accuracy=accuracy_results
    )