from fastapi import APIRouter, HTTPException
from app.models.models import TaskStatusResponseModel
from app.services.task import task_status
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/task/{task_id}", response_model=TaskStatusResponseModel)
async def get_task_status(task_id: str):
  try:
    if not task_id:
      raise HTTPException(status_code=404, detail="Please add task_id")
    result = await task_status(task_id)
    return result
  except Exception as e:
    #logger.error("Error in /extract/pdf")
    raise HTTPException(status_code=500, detail=str(e))


