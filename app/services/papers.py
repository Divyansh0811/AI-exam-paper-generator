import json
from bson import ObjectId
from fastapi import HTTPException
from app.models.models import PaperModel
from app.db.database import db, redis_client
from app.utils.utils import configure_logging

logger = configure_logging()

class PaperService:
    
    @staticmethod
    async def create_paper(request: PaperModel):
        try:
            paper_dict = request.dict()  # Convert request to dict
            result = await db.papers_db.insert_one(paper_dict)
            print(f"Result: {result}")
            paper_dict["_id"] = str(result.inserted_id)
            cached = redis_client.set(paper_dict["_id"], json.dumps(paper_dict))
            print(f"Caching paper {str(result.inserted_id)} in redis: {cached}")
            return paper_dict["_id"]
        except Exception as e:
            logger.error(f"Error in creating paper: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_paper(paper_id: str):
        try:
            if not ObjectId.is_valid(paper_id):
                raise HTTPException(status_code=400, detail=f"{paper_id} is not a valid ObjectId")

            cached_paper = redis_client.get(paper_id)
            if cached_paper:
                logger.info(f"Paper {paper_id} found in cache")
                return json.loads(cached_paper)
            print("Cache",cached_paper)
            paper = await db.papers_db.find_one({"_id": ObjectId(paper_id)})
            print("Paper",paper)
            if not paper:
              print("Here")
              raise HTTPException(
                status_code=404, detail=f"Paper with id:{paper_id} not found")
            print("now")
            paper["_id"] = str(paper["_id"])
            redis_client.set(paper_id, json.dumps(paper))
            return paper
        except Exception as e:
            logger.error(f"Error in retrieving paper: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update_paper(paper_id: str, request: PaperModel):
        try:
            if not ObjectId.is_valid(paper_id):
                raise HTTPException(status_code=400, detail=f"{paper_id} is not a valid ObjectId")

            existing_paper = await db.papers_db.find_one({"_id": ObjectId(paper_id)})
            if not existing_paper:
                raise HTTPException(status_code=404, detail=f"Paper with id {paper_id} not found")

            result = await db.papers_db.update_one({"_id": ObjectId(paper_id)}, {"$set": request.dict()})
            if result.modified_count == 0:
                return {"detail": f"No changes were made to the paper with id {paper_id}"}

            updated_paper = await db.papers_db.find_one({"_id": ObjectId(paper_id)})
            updated_paper["_id"] = str(updated_paper["_id"])
            invalidate_cache = redis_client.set(paper_id, json.dumps(updated_paper))
            logger.info(f"Invalidated cache for {paper_id}: {invalidate_cache}")
            return {"detail": f"Paper with id {paper_id} updated successfully"}
        except Exception as e:
            logger.error(f"Error in updating paper: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def delete_paper(paper_id: str):
        try:
            existing_paper = await db.papers_db.find_one({"_id": ObjectId(paper_id)})
            if not existing_paper:
                raise HTTPException(status_code=404, detail=f"Paper with id {paper_id} not found")

            result = await db.papers_db.delete_one({"_id": ObjectId(paper_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail=f"Paper ID: {paper_id} not found")

            redis_client.delete(paper_id)
            return {"detail": f"Paper with ID {paper_id} deleted successfully"}
        except Exception as e:
            logger.error(f"Error in deleting paper: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
