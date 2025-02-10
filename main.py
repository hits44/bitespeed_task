from fastapi import FastAPI , Depends, HTTPException
from database import get_db, Base, engine

from sqlalchemy.orm import Session
from db_services import create_contact, find_related_contacts, get_contact_by_id, get_all, update_contacts

# import models and init tables 
from models import Contact, LinkPrecedenceEnum

Base.metadata.create_all(bind=engine)
from pydantic import BaseModel


app = FastAPI()

class IdentifyPayload(BaseModel):
    phoneNumber: str = None
    email: str = None   

@app.post("/identify")
def identify_contact(payload: IdentifyPayload, db: Session = Depends(get_db)):
    """"""
    # get contacts by phone number

    # get contact by email

    # setup primary and make others secondary
    # cases
    # no entry exist -> creeate primary contact
    # relative contact exist -> 
        # 1 primary exist
            # got new entry -> create secondary with linkeed primary
            # same entry -> do nothing
        # multiple primary exist 
            # merge and make oldest as primary
                # got new entry -> create secondary with linkeed primary
                # same entry -> do nothing
    
    # check if one identifier is provided.
    if not payload.phoneNumber and not payload.email:
        raise HTTPException(status_code=400, detail="phoneNumber or email must be provided")
    

    
    # Update contacts according to our merge logic.
    primary_contact = update_contacts(db, payload.phoneNumber, payload.email)
    
    # Retrieve all related contacts for building the response.
    # related_contacts = find_related_contacts(db, payload.phoneNumber, payload.email)

    # Use the ORM relationship to get secondary contacts.
    secondary_contacts = primary_contact.secondary_contacts
    # import pdb;pdb.set_trace()
    # Combine the primary contact with its secondary contacts to build the full response.
    related_contacts = [primary_contact] + list(secondary_contacts)
    
    response = {"contact":{
        "primaryContactId": primary_contact.id,
        "emails": list({c.email for c in related_contacts if c.email}),
        "phoneNumbers": list({c.phoneNumber for c in related_contacts if c.phoneNumber}),
        "secondaryContactIds": [
            c.id for c in related_contacts if c.linkPrecedence == LinkPrecedenceEnum.secondary
        ]
    }}
    return response



@app.post("/contacts/add")
def create(db:Session =Depends(get_db),phoneNumber: str = None, email: str = None):
    # import pdb;pdb.set_trace()
    new_contact : Contact= create_contact(db=db, phoneNumber=phoneNumber, email=email)
    response = {"contact_id": new_contact.id, "phoneNumber": new_contact.phoneNumber, "email": new_contact.email}
    return response

@app.get("/contact/get")         
def get_contact(id , db=Depends(get_db)):
    contact = get_contact_by_id(id=id, db=db)
    return contact

@app.get("/contacts")
def getall(db= Depends(get_db)):
    return get_all(db)


