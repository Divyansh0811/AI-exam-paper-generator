from fastapi import APIRouter, HTTPException, UploadFile, File
from bson import ObjectId
import json
import logging

from app.models.models import PaperModel
from app.db.database import db, redis_client
from app.services.papers import PaperService
router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@router.post("/paper", response_model=dict)
async def create_sample_paper(request: PaperModel):
  try:
    paper_id = await PaperService.create_paper(request)
    return {"id": paper_id}
  except Exception as e:
    logger.error(f"Error in POST /papers: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))

@router.get("/paper/{paper_id}")
async def get_sample_paper(paper_id: str):
  try:
    paper = await PaperService.get_paper(paper_id)
    return paper
  except Exception as e:
    logger.error(f"Error in GET /paper/{paper_id}: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))

@router.put("/paper/{paper_id}", response_model=dict)
async def update_sample_paper(paper_id: str, request: PaperModel):
  try:
    updated_paper = await PaperService.update_paper(paper_id, request)
    return updated_paper
  except Exception as e:
    logger.error(f"Error in PUT /paper/{paper_id}: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))

@router.delete("/paper/{paper_id}")
async def delete_sample_paper(paper_id: str):
  try:
    deleted_paper = await PaperService.delete_paper(paper_id)
    return deleted_paper
  except Exception as e:
    logger.error(f"Error in DELETE /paper/{paper_id}: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))


