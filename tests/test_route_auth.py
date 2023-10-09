from unittest.mock import MagicMock

from src.database.models import User
from src.auth_services import create_email_token
from datetime import timedelta


def test_login_user(client, session, user):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"email": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_user_not_confirmed(client, session, user):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        '/api/auth/login',
        data={'email': user.get('email'), 'password': user.get('password')}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['token_type'] == 'bearer'


def test_login_wrong_email(client, user):
    response = client.post(
        "/api/auth/login",
        data={"email": 'email', "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"


def test_login_wrong_password(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": 'password'},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"

def test_create_email_token(self):
    data = {"sub": "test@example.com"}
    token = create_email_token(data, timedelta(minutes=15))
    self.assertIsNotNone(token)



