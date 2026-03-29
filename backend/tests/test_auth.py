from .conftest import TestingSessionLocal
from app.models import User, Role, UserStatus


def test_login_and_invite_accept(client):
    db = TestingSessionLocal()
    user = User(email="test@example.com", name="Test", role=Role.admin, status=UserStatus.invited)
    db.add(user)
    db.commit()
    db.close()

    response = client.post("/api/auth/invite/accept", json={"email": "test@example.com", "password": "pass123"})
    assert response.status_code == 200

    response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "pass123"})
    assert response.status_code == 200
