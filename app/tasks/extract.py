from app.celery import celery_app  # Import the centralized Celery app instance
import google.generativeai as genai
from app.config import settings
from app.constants import SCHEMA_EXTRACTION_PROMPT
from app.utils.utils import configure_logging

# Initialize logging
logger = configure_logging()

@celery_app.task(name="extract_pdf_task")
def extract_pdf_task(file_name: str):
    try:
        if not file_name:
            raise ValueError("Please provide a file name")

        # Configure generative AI and process the file
        genai.configure(api_key=settings.GEMINI_API_KEY)
        sample_pdf = genai.upload_file(file_name)
        llm = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = llm.generate_content([SCHEMA_EXTRACTION_PROMPT, sample_pdf])
        
        return response.text

    except Exception as e:
        logger.error("Error in extract_pdf_task")
        raise Exception(str(e))
