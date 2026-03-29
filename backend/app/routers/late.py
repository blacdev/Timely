from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import LateRequest, LateStatus, Role
from ..schemas import LateLog, LateDecision
from ..deps import get_current_user, require_role

router = APIRouter()


@router.post("/log")
def log_late(payload: LateLog, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    request = LateRequest(
        code=payload.code,
        user_id=payload.user_id,
        admin_target_user_id=payload.admin_target_user_id,
        eta_time=payload.eta_time,
        reason_text=payload.reason_text,
        status=LateStatus.logged,
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


@router.get("/pending")
def pending(db: Session = Depends(get_db), _user=Depends(require_role(Role.super_admin, Role.admin, Role.manager))):
    return db.query(LateRequest).filter(LateRequest.status == LateStatus.pending).all()


@router.post("/{late_id}/approve")
def approve(
    late_id: int,
    payload: LateDecision,
    db: Session = Depends(get_db),
    user=Depends(require_role(Role.super_admin, Role.admin, Role.manager)),
):
    request = db.query(LateRequest).filter(LateRequest.id == late_id).first()
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    request.status = LateStatus.approved
    request.decision_by = user.id
    request.decision_note = payload.note
    db.add(request)
    db.commit()
    return request


@router.post("/{late_id}/reject")
def reject(
    late_id: int,
    payload: LateDecision,
    db: Session = Depends(get_db),
    user=Depends(require_role(Role.super_admin, Role.admin, Role.manager)),
):
    request = db.query(LateRequest).filter(LateRequest.id == late_id).first()
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    request.status = LateStatus.rejected
    request.decision_by = user.id
    request.decision_note = payload.note
    db.add(request)
    db.commit()
    return request
