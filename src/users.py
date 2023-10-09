from sqlalchemy.orm import Session
from libgravatar import Gravatar
from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function is used to return contact from the database.
    :return: contact
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function is used to create new contact.
    :return: new user contact
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function is used to confirm a user's email address.
    It takes the email and get user by email and checks if user  confirmed or not.
   
    :param email: str: Get email
    :param db: Session: Pass the database session to the repository layer

    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function is used to update avatar.
    It takes the email and get user by email and checks if user  confirmed or not.
   
    :param email: str: Get email

    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user