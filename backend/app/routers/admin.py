from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Role, UserStatus
from ..schemas import UserCreate, UserOut, UserUpdate
from ..deps import require_role

router = APIRouter()


@router.post("/users", response_model=UserOut)
def invite_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin, Role.admin, Role.manager)),
):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User exists")
    user = User(
        email=payload.email,
        name=payload.name,
        role=payload.role,
        status=UserStatus.invited,
        invited_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin, Role.admin, Role.manager)),
):
    return db.query(User).all()


@router.patch("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin, Role.admin)),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", response_model=UserOut)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _user=Depends(require_role(Role.super_admin, Role.admin)),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.status = UserStatus.disabled
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
