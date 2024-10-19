# app/main.py
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import redis
import os
from app.router import papers, extract, task
from app.config import settings
from fastapi.responses import JSONResponse
from app.db.database import db, redis_client
import logging

app = FastAPI(title="Sample Paper API", version="1.0.0")

# Include routers
app.include_router(papers.router)
app.include_router(task.router)
app.include_router(extract.router, prefix="/extract")


# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/", summary="Health Check Endpoint")
async def root():
    logger.info("Health check endpoint accessed.")
    return JSONResponse(content={"message": "API is up and running! 🟢"})

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return JSONResponse(content={"message": "Swagger UI is available at /docs"})


@app.get("/test_mongo", summary="MongoDB connection")
async def test_mongo():
  try:
    user = settings.MONGO_INITDB_ROOT_USERNAME
    password = settings.MONGO_INITDB_ROOT_PASSWORD

    client = AsyncIOMotorClient(f'mongodb://{user}:{password}@mongodb:27017/?authSource=admin')
    db = client["papers_db"]
    await db.command("ping")
    
    return {"message": "MongoDB connected succesfully"}
  except Exception as e:
    logger.error("MongoDB connection failed")
    raise HTTPException(status_code=500, detail=str(e))

@app.get("/test_redis", summary="Redis connection")
async def test_redis():
  try:
    redis_client = redis.StrictRedis(
        host='redis',  # Use the service name defined in docker-compose
        port=6379,
        decode_responses=True,
        db=0
      )
    await redis_client.ping()
    return {"status": "Redis connection successfull"}
  except Exception as e:
    logger.error("REdis connection failed")
    raise HTTPException(status_code=500, detail=str(e))
