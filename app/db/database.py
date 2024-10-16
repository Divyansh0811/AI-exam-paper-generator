from motor.motor_asyncio import AsyncIOMotorClient
import redis
import os
from app.config import settings


user = settings.MONGO_INITDB_ROOT_USERNAME
password = settings.MONGO_INITDB_ROOT_PASSWORD

client = AsyncIOMotorClient(f'mongodb://{user}:{password}@mongodb:27017/?authSource=admin')
db = client["papers_db"]

redis_client = redis.StrictRedis(
    host='redis',  # Use the service name defined in docker-compose
    port=6379,
    decode_responses=True,
    db=0
)