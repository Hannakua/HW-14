import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app

from sqlalchemy.orm import Session
from libgravatar import Gravatar

from src.database.models import User
from src.schemas import UserModel
from src.users import (
    confirmed_email,
    update_token,
    update_avatar,
  )


client = TestClient(app)

class TestRepositoryUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.body = UserModel(
            email="post@emeta.ua",
            password="simple123",
        )

    async def test_confirmed_email(self):
        user = User(id=1)
        email_=user.email
        result = await confirmed_email(email_, self.session)
        self.assertIsNone(result)
        self.assertTrue(user.confirmed)
        self.session.commit.assert_called_once()


    async def test_update_avatar(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user
        user = User(id=1)
        email_=user.email
        result = await update_avatar(email_, url="new_avatar_url", db=self.session)
        self.assertEqual(result, mock_user)
        self.session.commit.assert_called_once()

    async def test_update_token(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user
        new_token = "new_token"
        result = await update_token(user=mock_user, token=new_token, db=self.session)
        self.assertIsNone(result)
        self.assertEqual(mock_user.refresh_token, new_token)
        self.session.commit.assert_called_once()