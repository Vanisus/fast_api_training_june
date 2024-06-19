from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from tasks.tasks import send_email_report_dashboard

from auth.base_config import current_user

router = APIRouter(prefix='/report',
                   tags=['Reports'])


@router.get('/dashboard')
def get_dashboard_report(user=Depends(current_user)):
    send_email_report_dashboard(user.username)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }