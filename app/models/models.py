from fastapi import HTTPException
from pydantic import BaseModel, Field, conint, validator
from typing import List, Optional, Dict
import bleach # To sanitize input
import os

def sanitize_input(input: str) -> str:
  return bleach.clean(input, strip=True)
class QuestionModel(BaseModel):
  question: str
  answer: str
  type: str
  question_slug: str
  reference_id: str
  hint: str
  params: Dict[str, str]

  @validator('question', 'answer', 'hint', 'question_slug', 'reference_id', 'type')
  def sanitize_question_fields(cls, value):
    return sanitize_input(value)

class ParamsModel(BaseModel):
  board: str
  grade: conint(gt=1)
  subject: str

  @validator('board', 'subject')
  def santize_params_fields(cls, value):
    return sanitize_input(value)

class SectionModel(BaseModel):
  marks_per_question: conint(gt=0)
  type: str
  questions: List[QuestionModel]

  @validator('type')
  def sanitize_section_fields(cls, value):
    return sanitize_input(value)
  
class PaperModel(BaseModel):
  title: str
  type: str
  time: conint(gt=0)
  marks: conint(gt=0)
  params: ParamsModel
  tags: List[str]
  chapters: List[str]
  sections: List[SectionModel]

  @validator('title', 'type', 'tags', 'chapters')
  def sanitize_paper_fields(cls, value):
    if isinstance(value, list):
      return [sanitize_input(v) for v in value]
    return sanitize_input(value)

class ExtractionPDFModel(BaseModel):
  file_name: str = Field(..., description = "Name of the PDF file to be extracted")

  @validator("file_name")
  def check_file_exists(cls, value):
    file_name_with_extension = value + ".pdf"
    print("Value -> ", file_name_with_extension)
    file_path = os.path.join(os.getcwd(), file_name_with_extension) 
    print(os.getcwd())
    if not os.path.exists(file_path):
      raise HTTPException(status_code=404, detail="File doesn't exists in the current directory")
    return file_name_with_extension

  @validator('file_name')
  def sanitize_extract_pdf_fields(cls, value):
    return sanitize_input(value)

class ExtractTextModel(BaseModel):
  user_input: str = Field(..., description="Text input to be extracted")

  @validator('user_input')
  def sanitize_text_fields(cls, value):
    return sanitize_input(value)