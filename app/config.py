from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  MONGODB_URL: str
  REDIS_URL: str
  GEMINI_API_KEY: str
  CELERY_BROKER_URL: str
  CELERY_RESULT_BACKEND: str
  MONGO_INITDB_ROOT_USERNAME: str
  MONGO_INITDB_ROOT_PASSWORD: str

  class Config:
    env_file = ".env"

settings = Settings()