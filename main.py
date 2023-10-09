from fastapi import FastAPI, Depends, status, HTTPException, Query
from src.database.db import get_db
from sqlalchemy.orm import Session
from src.schemas import ContactResponse, ContactUpdate, ContactBase
from src.database.models import Contact, User
from typing import List
from datetime import date, timedelta
from src.auth_services import auth_service
from src.auth_routes import router
from src.routes_users import router_users
import redis.asyncio as redis
from src.conf.config import settings
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from src.conf.config import settings

app = FastAPI()

app.include_router(router, prefix='/api')
app.include_router(router_users, prefix='/api')

origins = [settings.origins_url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/contacts/{params}", response_model=list[ContactResponse], tags=['contacts'])
async def search_contacts(
    db: Session = Depends(get_db),
    firstname_: str = Query(None, description="Firstname: "),
    lastname_: str = Query(None, description="Lastname: "),
    email_: str = Query(None, description="Email: "),
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    The search_contacts function is used to search contacts from the database.
    :return: contact
    """       
    if firstname_:
        contacts = db.query(Contact).filter(Contact.firstname==firstname_, Contact.user_id==current_user.id).all()
    elif lastname_:
        contacts = db.query(Contact).filter(Contact.lastname==lastname_, Contact.user_id==current_user.id).all()
    elif email_:
        contacts = db.query(Contact).filter(Contact.email==email_, Contact.user_id==current_user.id).all()
    else:
        contacts = db.query(Contact).filter(Contact.user_id==current_user.id).all()

    return contacts

@app.post("/contacts", response_model=ContactResponse, tags=["contacts"])
async def create_contact(body: ContactBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Pass the contact data to the function
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user id from the jwt token
    :return: The created contact
    """
    contact = Contact(**body.model_dump(), user_id=current_user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

@app.get("/contacts", response_model=list[ContactResponse], tags=['contacts'])
async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function is used to read contacts from the database.
    :return: A list of contacts
    """
    contacts = db.query(Contact).filter(Contact.user_id==current_user.id).all()
    return contacts    

@app.get("/contacts/{contact_id}", response_model=ContactResponse, tags=['contacts'])
async def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function is used to retrieve a single contact from the database.
    
    :param contact_id: int: Specify the id of the contact we want to update
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    """
    contact = db.query(Contact).filter(id==contact_id, Contact.user_id==current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact 

@app.patch("/contacts/{contact_id}", response_model=ContactResponse, tags=['contacts'])
async def update_contact(
    contact_id: int, body: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)
):
    """
    The update_contact function updates a contact in the database.
    Params:
    body: A ContactPartialUpdateModel object containing the fields to be updated and their new values.
    contact_id: An integer representing the ID of the contact to be updated.
    db (optional): A Session object for interacting with an SQLAlchemy database session pool, if not provided, one will be created automatically using Depends(get_db).

    :param body: ContactPartialUpdateModel: Specify the type of data that will be passed in the body
    :param contact_id: int: Specify the contact that is to be deleted
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the auth_service
    :return: A contact model
    """
    contact = (db.query(Contact).filter(id==contact_id, Contact.user_id==current_user.id).first()
    )
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    contact.email = body.email
    contact.phone = body.phone

    db.commit()
    return contact  

@app.get("/contacts/{birthday}", response_model=list[ContactResponse], tags=['contacts'])
async def get_birthday(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Get a list of contacts whose birthday falls within the selected time period. The period for 7 days.

    """
    todaydate = date.today()
    nextdate = todaydate + timedelta(days=6)

    contact = (db.query(Contact).filter(((Contact.birthdate) <= nextdate)&((Contact.birthdate) >= todaydate), Contact.user_id==current_user.id).all())
    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contact


@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['contacts'])
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the contact to be removed
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user that is currently logged in
    :return: The contact that has been removed
    """
    contact = (db.query(Contact).filter(id==contact_id, Contact.user_id==current_user.id).first()
    )
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return contact


