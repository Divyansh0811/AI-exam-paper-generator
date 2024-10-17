from fastapi import HTTPException
import logging
from celery.result import AsyncResult

logger = logging.getLogger(__name__)
class TaskService:

  async def task_status(task_id):

      try:
          result = AsyncResult(task_id)
          
          if result.state == "PENDING":
              response = {
                  "task_id": task_id,
                  "status": result.state,
                  "info": "Task is still pending...",
              }
          elif result.state == "PROGRESS":
              response = {
                  "task_id": task_id,
                  "status": result.state,
                  "info": result.info or "Task in progress",
              }
          elif result.state == "SUCCESS":
              # Retrieve the result once the task is successful
              response = {
                  "task_id": task_id,
                  "status": result.state,
                  "result": str(result.result)  # Ensure result is handled as a string
              }
          elif result.state == "FAILURE":
              response = {
                  "task_id": task_id,
                  "status": result.state,
                  "error": str(result.info) or "Unknown error occurred",
              }
          else:
              response = {
                  "task_id": task_id,
                  "status": result.state,
                  "info": "Unknown state",
              }
          
          return response
      except Exception as e:
          #logger.error("Error fetching task status", exc_info=True)
          raise HTTPException(status_code=500, detail=str(e))