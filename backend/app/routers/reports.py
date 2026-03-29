import os
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from openpyxl import Workbook
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AttendanceDay, ReportRun, User, Role, ReportStatus
from ..deps import require_role

router = APIRouter()
REPORT_DIR = os.getenv("REPORT_DIR", "/workspace/Timely/backend/reports")


@router.post("/monthly/generate")
def generate_monthly(
    month: str,
    db: Session = Depends(get_db),
    user=Depends(require_role(Role.super_admin, Role.admin)),
):
    os.makedirs(REPORT_DIR, exist_ok=True)
    run = ReportRun(month=month, status=ReportStatus.pending, generated_by_user_id=user.id)
    db.add(run)
    db.commit()
    db.refresh(run)

    workbook = Workbook()
    workbook.remove(workbook.active)
    users = db.query(User).all()
    for u in users:
        sheet = workbook.create_sheet(title=u.name[:30])
        sheet.append(["Date", "Clock In", "Clock Out", "Status"])
        rows = (
            db.query(AttendanceDay)
            .filter(AttendanceDay.user_id == u.id, AttendanceDay.work_date.like(f"{month}%"))
            .all()
        )
        for row in rows:
            sheet.append([row.work_date.isoformat(), str(row.clock_in_at), str(row.clock_out_at), row.status.value])
    filename = os.path.join(REPORT_DIR, f"monthly-{month}.xlsx")
    workbook.save(filename)
    run.status = ReportStatus.completed
    run.files_meta_json = {"monthly": filename}
    db.add(run)
    db.commit()
    return {"status": "ok", "file": filename}


@router.get("/monthly/download")
def download_monthly(
    month: str,
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin, Role.admin, Role.manager)),
):
    run = db.query(ReportRun).filter(ReportRun.month == month, ReportRun.status == ReportStatus.completed).first()
    if not run or not run.files_meta_json:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    path = run.files_meta_json.get("monthly")
    return FileResponse(path, filename=os.path.basename(path))


@router.get("/user/download")
def download_user(user_id: int, month: str, db: Session = Depends(get_db), _user=Depends(require_role(Role.super_admin, Role.admin))):
    run = db.query(ReportRun).filter(ReportRun.month == month, ReportRun.status == ReportStatus.completed).first()
    if not run or not run.files_meta_json:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return FileResponse(run.files_meta_json.get("monthly"), filename=f"user-{user_id}-{month}.xlsx")
