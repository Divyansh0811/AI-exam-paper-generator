from fastapi import APIRouter, HTTPException
from app.models.models import ExtractionPDFModel, ExtractTextModel
from app.services.extract import ExtractionService
from app.tasks.extract import extract_pdf_task  # Import the Celery task
from app.utils.utils import configure_logging

router = APIRouter()

logger = configure_logging()
@router.post("/pdf")
async def extract_from_pdf(request: ExtractionPDFModel):
    try:
        # Initiate the asynchronous task
        task = extract_pdf_task.delay(request.file_name)  
        
        # Return the task ID so the client can check the status
        return {"task_id": task.id}  
    except Exception as e:
        logger.error("Error in /extract/pdf")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/text")
async def extract_from_text(request: ExtractTextModel):
  try:
    result = await ExtractionService.extract_text(request.user_input)
    return result
  except Exception as e:
    logger.error("Error in /extract/text")
    raise HTTPException(status_code=500, detail=str)
