from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import OrgSettings, Schedule, Role
from ..schemas import OrgSettingsOut, OrgSettingsUpdate, ScheduleUpdate
from ..deps import require_role

router = APIRouter()


@router.get("/rules", response_model=OrgSettingsOut)
def get_rules(
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin, Role.admin)),
):
    settings = db.query(OrgSettings).first()
    if not settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found")
    return settings


@router.put("/rules", response_model=OrgSettingsOut)
def update_rules(
    payload: OrgSettingsUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin)),
):
    settings = db.query(OrgSettings).first()
    if not settings:
        settings = OrgSettings(**payload.dict())
    else:
        for field, value in payload.dict().items():
            setattr(settings, field, value)
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


@router.get("/schedules/{user_id}")
def get_schedule(
    user_id: int,
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin, Role.admin, Role.manager)),
):
    return db.query(Schedule).filter(Schedule.user_id == user_id).all()


@router.put("/schedules/{user_id}")
def update_schedule(
    user_id: int,
    payload: ScheduleUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin, Role.admin, Role.manager)),
):
    db.query(Schedule).filter(Schedule.user_id == user_id).delete()
    for entry in payload.entries:
        db.add(Schedule(user_id=user_id, weekday=entry.weekday, start_time=entry.start_time, end_time=entry.end_time))
    db.commit()
    return {"status": "ok"}
