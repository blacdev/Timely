from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AttendanceDay, Device, AttendanceStatus, Role
from ..schemas import ClockRequest, AttendanceOut, AttendanceCorrection
from ..deps import get_current_user, require_role
from .auth import verify_nonce, verify_signature

router = APIRouter()


@router.post("/attendance/clock-in", response_model=AttendanceOut)
def clock_in(
    payload: ClockRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    device = db.query(Device).filter(Device.id == payload.device_id, Device.user_id == user.id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    verify_nonce(device.id, payload.nonce, payload.signature)
    verify_signature(device.device_secret_hash, payload.nonce, payload.signature)
    today = date.today()
    record = db.query(AttendanceDay).filter(AttendanceDay.user_id == user.id, AttendanceDay.work_date == today).first()
    if not record:
        record = AttendanceDay(user_id=user.id, work_date=today)
    record.clock_in_at = datetime.utcnow()
    record.status = AttendanceStatus.incomplete
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post("/attendance/clock-out", response_model=AttendanceOut)
def clock_out(
    payload: ClockRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    device = db.query(Device).filter(Device.id == payload.device_id, Device.user_id == user.id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    verify_nonce(device.id, payload.nonce, payload.signature)
    verify_signature(device.device_secret_hash, payload.nonce, payload.signature)
    today = date.today()
    record = db.query(AttendanceDay).filter(AttendanceDay.user_id == user.id, AttendanceDay.work_date == today).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No clock-in found")
    record.clock_out_at = datetime.utcnow()
    record.status = AttendanceStatus.on_time
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/attendance/me/month", response_model=list[AttendanceOut])
def my_month(
    yyyy_mm: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    year, month = map(int, yyyy_mm.split("-"))
    return (
        db.query(AttendanceDay)
        .filter(
            AttendanceDay.user_id == user.id,
            AttendanceDay.work_date.between(date(year, month, 1), date(year, month, 28)),
        )
        .all()
    )


@router.get("/admin/attendance", response_model=list[AttendanceOut])
def admin_attendance(
    range: str,
    user: int | None = None,
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin, Role.admin, Role.manager)),
):
    start_str, end_str = range.split("/")
    start_date = date.fromisoformat(start_str)
    end_date = date.fromisoformat(end_str)
    query = db.query(AttendanceDay).filter(AttendanceDay.work_date.between(start_date, end_date))
    if user:
        query = query.filter(AttendanceDay.user_id == user)
    return query.all()


@router.post("/admin/attendance/{attendance_id}/correct", response_model=AttendanceOut)
def correct_attendance(
    attendance_id: int,
    payload: AttendanceCorrection,
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin, Role.admin)),
):
    record = db.query(AttendanceDay).filter(AttendanceDay.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
    record.clock_in_at = payload.clock_in_at
    record.clock_out_at = payload.clock_out_at
    record.status = payload.status
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
