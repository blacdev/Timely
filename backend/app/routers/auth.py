import hmac
import hashlib
import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Device, UserStatus
from ..schemas import Token, InviteAccept, ChallengeRequest, ChallengeResponse
from ..auth import verify_password, create_access_token, hash_password

router = APIRouter()

_nonce_store = {}


@router.post("/login", response_model=Token)
def login(payload: InviteAccept, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(str(user.id))
    return Token(access_token=token)


@router.post("/invite/accept", response_model=Token)
def accept_invite(payload: InviteAccept, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or user.status == UserStatus.disabled:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
    user.password_hash = hash_password(payload.password)
    user.status = UserStatus.active
    db.add(user)
    db.commit()
    token = create_access_token(str(user.id))
    return Token(access_token=token)


@router.post("/challenge", response_model=ChallengeResponse)
def challenge(payload: ChallengeRequest, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == payload.device_id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    nonce = secrets.token_hex(16)
    expires_at = datetime.utcnow() + timedelta(seconds=30)
    _nonce_store[nonce] = {"device_id": device.id, "expires_at": expires_at}
    return ChallengeResponse(nonce=nonce, expires_at=expires_at)


def verify_nonce(device_id: int, nonce: str, signature: str) -> None:
    entry = _nonce_store.get(nonce)
    if not entry or entry["device_id"] != device_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid nonce")
    if datetime.utcnow() > entry["expires_at"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nonce expired")
    _nonce_store.pop(nonce, None)


def verify_signature(secret: str, nonce: str, signature: str) -> None:
    expected = hmac.new(secret.encode(), nonce.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
