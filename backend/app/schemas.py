from datetime import datetime, date, time
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr
from .models import Role, UserStatus, AttendanceStatus, LateStatus


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    role: Role


class UserUpdate(BaseModel):
    name: Optional[str]
    role: Optional[Role]
    status: Optional[UserStatus]


class UserOut(UserBase):
    id: int
    role: Role
    status: UserStatus

    class Config:
        orm_mode = True


class InviteAccept(BaseModel):
    email: EmailStr
    password: str


class ChallengeRequest(BaseModel):
    device_id: int


class ChallengeResponse(BaseModel):
    nonce: str
    expires_at: datetime


class ClockRequest(BaseModel):
    device_id: int
    nonce: str
    signature: str


class AttendanceOut(BaseModel):
    id: int
    work_date: date
    clock_in_at: Optional[datetime]
    clock_out_at: Optional[datetime]
    status: AttendanceStatus

    class Config:
        orm_mode = True


class AttendanceCorrection(BaseModel):
    clock_in_at: Optional[datetime]
    clock_out_at: Optional[datetime]
    status: AttendanceStatus
    reason: str


class LateLog(BaseModel):
    code: str
    user_id: int
    admin_target_user_id: Optional[int]
    eta_time: Optional[time]
    reason_text: Optional[str]


class LateDecision(BaseModel):
    note: Optional[str]


class OrgRules(BaseModel):
    late_threshold: int
    early_threshold: int
    absent_threshold: int
    rounding: str


class OrgSettingsOut(BaseModel):
    allowed_domain: str
    server_base_url: str
    timezone: str
    rules_json: Dict[str, Any]


class OrgSettingsUpdate(BaseModel):
    allowed_domain: str
    server_base_url: str
    timezone: str
    rules_json: Dict[str, Any]


class ScheduleEntry(BaseModel):
    weekday: int
    start_time: time
    end_time: time


class ScheduleUpdate(BaseModel):
    entries: List[ScheduleEntry]
