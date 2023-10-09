import unittest
from unittest.mock import MagicMock
from datetime import timedelta, date

from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schemas import ContactUpdate, ContactBase, ContactResponse
from main import (
    get_contact,
    get_contacts,
    get_birthday,
    remove_contact 
)

class TestContacts(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(db=self.session, user=self.user)
        self.assertEqual(result, contacts)
    
    async def test_get_contact_by_id_found(self):
        mock_contact = Contact()
        self.session.query().filter().first.return_value = mock_contact
        result = await get_contact(contact_id=1, db=self.session, user=self.user)
        self.assertEqual(result, mock_contact)

    async def test_get_contact_by_id_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_get_birthdays(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.execute.return_value.scalars.return_value.all.return_value = contacts
        result = await get_birthday(db=self.session, user=self.user)
        self.assertEqual(result, contacts)

    async def test_remove_contact_found(self):
        mock_contact = Contact()
        self.session.query().filter().first.return_value = mock_contact
        result = await remove_contact(contact_id=1, db=self.session, user=self.user)
        self.assertEqual(result, mock_contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(user=self.user, contact_id=1, db=self.session)
        self.assertIsNone(result)

    
if __name__ == '__main__':
    unittest.main()