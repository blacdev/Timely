import enum
from datetime import datetime, date, time
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Time,
    Boolean,
    ForeignKey,
    Enum,
    Text,
    UniqueConstraint,
    JSON,
)
from sqlalchemy.orm import relationship
from .database import Base


class Role(str, enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    manager = "manager"
    user = "user"


class UserStatus(str, enum.Enum):
    active = "active"
    disabled = "disabled"
    invited = "invited"


class AttendanceStatus(str, enum.Enum):
    on_time = "on_time"
    late = "late"
    early = "early"
    absent = "absent"
    incomplete = "incomplete"


class LateStatus(str, enum.Enum):
    logged = "logged"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ReportStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class OrgSettings(Base):
    __tablename__ = "org_settings"

    id = Column(Integer, primary_key=True)
    allowed_domain = Column(String, nullable=False)
    server_base_url = Column(String, nullable=False)
    timezone = Column(String, nullable=False, default="UTC")
    rules_json = Column(JSON, nullable=False, default=dict)
    smtp_json_encrypted = Column(Text, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.user)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.invited)
    password_hash = Column(String, nullable=True)
    invited_at = Column(DateTime, default=datetime.utcnow)

    devices = relationship("Device", back_populates="user")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_label = Column(String, nullable=False)
    device_secret_hash = Column(String, nullable=False)
    last_seen_at = Column(DateTime)

    user = relationship("User", back_populates="devices")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weekday = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "weekday", name="uq_schedule_user_day"),)


class AttendanceDay(Base):
    __tablename__ = "attendance_days"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    work_date = Column(Date, nullable=False)
    scheduled_start = Column(Time)
    scheduled_end = Column(Time)
    clock_in_at = Column(DateTime)
    clock_out_at = Column(DateTime)
    status = Column(Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.incomplete)
    minutes_late = Column(Integer, default=0)
    minutes_early = Column(Integer, default=0)
    hours_worked = Column(Integer, default=0)
    source = Column(String, default="mobile")

    __table_args__ = (UniqueConstraint("user_id", "work_date", name="uq_attendance_user_date"),)


class AttendanceAudit(Base):
    __tablename__ = "attendance_audit"

    id = Column(Integer, primary_key=True)
    attendance_day_id = Column(Integer, ForeignKey("attendance_days.id"), nullable=False)
    changed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    diff_json = Column(JSON, nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class LateRequest(Base):
    __tablename__ = "late_requests"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    admin_target_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    eta_time = Column(Time, nullable=True)
    reason_text = Column(Text, nullable=True)
    status = Column(Enum(LateStatus), nullable=False, default=LateStatus.logged)
    decision_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    decision_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ReportRun(Base):
    __tablename__ = "report_runs"

    id = Column(Integer, primary_key=True)
    month = Column(String, nullable=False)
    status = Column(Enum(ReportStatus), nullable=False, default=ReportStatus.pending)
    generated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    files_meta_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
