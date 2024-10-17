from fastapi import HTTPException
import google.generativeai as genai
from app.config import settings
from app.constants import SCHEMA_EXTRACTION_PROMPT
import logging 


def configure_logging():
  # Configure Logging
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  return logger

logger = configure_logging()

async def extract_pdf(file_name: str):
    try:
        if not file_name:
          raise HTTPException(status_code=400, detail="Please provide a file name")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        sample_pdf = genai.upload_file(file_name)
        llm = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        response = await llm.generate_content([SCHEMA_EXTRACTION_PROMPT, sample_pdf])
        return response.text
    except Exception as e:
        logger.error("Error in extract_pdf", exc_info=True)  # Logs exception details
        raise HTTPException(status_code=500, detail=str(e))