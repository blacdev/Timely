from app.database import SessionLocal, engine
from app.models import Base, User, Role, UserStatus
from app.auth import hash_password


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    email = "admin@local"
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print("Super admin already exists")
        return
    user = User(
        email=email,
        name="Super Admin",
        role=Role.super_admin,
        status=UserStatus.active,
        password_hash=hash_password("change-me"),
    )
    db.add(user)
    db.commit()
    print("Created super admin: admin@local / change-me")


if __name__ == "__main__":
    main()
