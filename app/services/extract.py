from fastapi import HTTPException
import google.generativeai as genai
from app.config import settings
from app.constants import SCHEMA_EXTRACTION_PROMPT
from app.utils.utils import configure_logging
from app.celery import celery_app

logger = configure_logging()
class ExtractionService:

  @celery_app.task  
  async def extract_pdf(file_name: str):
    try:
      print("File name ->", file_name)
      if not file_name:
        raise HTTPException(status_code=400, detail = "Please provide a file name")
      genai.configure(api_key=settings.GEMINI_API_KEY)
      sample_pdf = genai.upload_file(file_name)
      llm = genai.GenerativeModel(model_name="gemini-1.5-flash")
      response = llm.generate_content([SCHEMA_EXTRACTION_PROMPT, sample_pdf])
      print(response)
      return response.text
    except Exception as e:
      logger.error("Error in extract_pdf")
      raise HTTPException(status_code=500, detail=str(e))

  async def extract_text(user_input: str):
    try:
      genai.configure(api_key=settings.GEMINI_API_KEY)
      llm = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SCHEMA_EXTRACTION_PROMPT)
      print(llm)
      response = llm.generate_content(user_input)
      print(response)
      return response.text
    except Exception as e:
      logger.error("Error in extract_text")
      raise HTTPException(status_code=500, detail=str(e))