from fastapi import APIRouter, HTTPException
from app.tasks.extract import extract_pdf_task  # Import the task to track its status
from app.utils.utils import configure_logging

router = APIRouter()
logger = configure_logging()

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    Fetch the status and result of a task by its task_id.
    """
    try:
        task = extract_pdf_task.AsyncResult(task_id)  # Fetch the task status using task ID

        if task.state == 'PENDING':
            return {"status": "Pending", "result": None}
        elif task.state == 'SUCCESS':
            return {"status": "Completed", "result": task.result}
        elif task.state == 'FAILURE':
            return {"status": "Failed", "error": str(task.info)}
        else:
            return {"status": task.state, "result": None}

    except Exception as e:
        logger.error(f"Error fetching task status for task_id {task_id}")
        raise HTTPException(status_code=500, detail=str(e))
