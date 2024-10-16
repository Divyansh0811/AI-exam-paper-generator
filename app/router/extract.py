from fastapi import APIRouter, HTTPException
from app.models.models import ExtractionPDFModel, ExtractTextModel
from app.services.extract import extract_pdf, extract_text
from app.utils.utils import configure_logging

router = APIRouter()

logger = configure_logging()

@router.post("/pdf")
async def extract_from_pdf(request: ExtractionPDFModel):
  try:
    result = await extract_pdf(request.file_name)
    return result
  except Exception as e:
    logger.error("Error in /extract/pdf")
    raise HTTPException(status_code=500, detail=str(e))

@router.get("/text")
async def extract_from_text(request: ExtractTextModel):
  try:
    result = await extract_text(request.user_input)
    return result
  except Exception as e:
    logger.error("Error in /extract/text")
    raise HTTPException(status_code=500, detail=str)
