from fastapi import APIRouter, HTTPException, UploadFile, File
from bson import ObjectId
import json
import logging

from app.models.models import PaperModel
from app.db.database import db, redis_client

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/papers", response_model=dict)
async def create_sample_paper(paper: PaperModel):
    try:
        paper_dict = paper.dict()  # Convert Pydantic model to dict
        # Insert the paper into MongoDB
        result = await db.papers_db.insert_one(paper_dict)
        # Convert ObjectId to string for the response
        paper_dict["_id"] = str(result.inserted_id)
        # Cache the inserted paper
        await redis_client.set(paper_dict["_id"], json.dumps(paper_dict))
        return {"id": paper_dict["_id"]}
    except Exception as e:
        logger.error("Error in create_sample_paper, details: ", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/paper/{paper_id}")
async def get_sample_paper(paper_id: str):
    try:
        if not ObjectId.is_valid(paper_id):
            raise HTTPException(
                status_code=400, detail=f"{paper_id} is not a valid ObjectId")

        # Check Redis cache first
        cached_paper = await redis_client.get(paper_id)
        if cached_paper:
            logger.info(f"Found paper in cache, id: {paper_id}")
            return json.loads(cached_paper)

        # Fetch the paper from MongoDB
        object_id = ObjectId(paper_id)
        paper = await db.papers_db.find_one({"_id": object_id})
        if not paper:
            raise HTTPException(
                status_code=404, detail=f"Paper with id:{paper_id} not found")

        paper["_id"] = str(paper["_id"])  # Convert ObjectId to string
        await redis_client.set(paper_id, json.dumps(paper))  # Cache the paper
        return paper  # Return the paper
    except Exception as e:
        logger.error("Error in get_sample_paper, details: ", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/paper/{paper_id}")
async def update_sample_paper(paper_id: str, paper: PaperModel):
    try:
        if not ObjectId.is_valid(paper_id):
            raise HTTPException(
                status_code=400, detail=f"{paper_id} is not a valid ObjectId")

        # Check if the paper exists
        existing_paper = await db.papers_db.find_one({"_id": ObjectId(paper_id)})
        if not existing_paper:
            raise HTTPException(
                status_code=404, detail=f"Paper with id={paper_id} not found")

        # Update the paper in the database
        result = await db.papers_db.update_one({"_id": ObjectId(paper_id)}, {"$set": paper.dict()})
        if result.modified_count == 0:
            return {"detail": f"No changes were made to the paper with id: {paper_id}"}

        # Update Redis cache
        # Fetch updated paper
        updated_paper = await db.papers_db.find_one({"_id": ObjectId(paper_id)})
        # Convert ObjectId to string
        updated_paper["_id"] = str(updated_paper["_id"])
        # Cache the updated paper
        await redis_client.set(paper_id, json.dumps(updated_paper))

        return {"detail": f"Paper with id: {paper_id} updated successfully"}
    except Exception as e:
        logger.error("Error in update_sample_paper, details: ", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/paper/{paper_id}")
async def delete_sample_paper(paper_id: str):
    try:
        if not paper_id:
            raise HTTPException(status_code=400, detail="Paper ID is required")

        existing_paper = db.paper_db.find_one({"_id": ObjectId(paper_id)})
        if not existing_paper:
            raise HTTPException(
                status_code=404, detail=f"Paper with id: {paper_id} not found")

        result = await db.papers_db.delete_one({"_id": ObjectId(paper_id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404, detail=f"Paper ID: {paper_id} not found")
        await redis_client.delete(paper_id)
        return {"detail": f"Paper with ID: {paper_id} deleted successfully"}
    except Exception as e:
        logger.error("Error in delete_sample_paper, details: ")
        raise HTTPException(status_code=500, detail=str(e))
