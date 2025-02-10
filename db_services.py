from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models import Contact, LinkPrecedenceEnum
from datetime import datetime


def find_related_contacts(db : Session, phone_number: str =None, email: str = None ):
    filters = []
    if phone_number:
        filters.append(Contact.phoneNumber==phone_number)
    if phone_number:
        filters.append(Contact.email==email)

    if not filters:
        # if no filter to query wee return nothing
        return []

    related_contacts = db.query(Contact).filter(or_(*filters)).all()
    return related_contacts

def find_contact(db: Session, phone, email):
    contacts= db.query(Contact).filter(and_(Contact.phoneNumber==phone,Contact.email==email)).all()
    if len(contacts)>1:
        raise Exception("multiple same contacts found.")
    if contacts:
        return contacts[0]

def create_contact(db: Session, **params) -> Contact:
    new_contact = Contact(
        phoneNumber = params.get("phoneNumber"),
        email= params.get("email"),
        linkPrecedence=params.get("linkPrecedence", LinkPrecedenceEnum.primary),
        linkedId=params.get("linkedId"),
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

def get_contact_by_id(db:Session, id):
    c= db.query(Contact).get(id)
    return c

def get_all(db:Session):
    return db.query(Contact).all()

def find_oldest_primary_contact(contacts):
    """Return the contact with the earliest createdAt timestamp."""
    # assuming we have primary contact as the oldest and if its deleted we setup another primary
    return min(contacts, key=lambda c: c.createdAt)
    

def update_to_secondary(db: Session, primary_contact: Contact, contacts: list):
    """For all contacts (except the primary), update them to be secondary and link to primary_contact."""
    updated_secondary_contacts = []
    for contact in contacts:
        if (contact.id != primary_contact.id) and (
            contact.linkPrecedence != LinkPrecedenceEnum.secondary or 
            contact.linkedId != primary_contact.id):
                
            contact.linkPrecedence = LinkPrecedenceEnum.secondary
            contact.linkedId = primary_contact.id
            contact.updatedAt = datetime.now()
            updated_secondary_contacts.append(contact)

    db.add_all(updated_secondary_contacts)


def update_contacts(db: Session, phone, email):
    """update oldest primary contact to """
    same_contact = find_contact(db, phone, email)
    if same_contact:
        same_contact.updatedAt = datetime.now()
        db.add(same_contact)
        db.commit()
        db.refresh(same_contact)
    else:
        # creeatee contact as primary and will be set secondary later stage if not primary
        new_contact  = create_contact(db=db, phoneNumber=phone,email=email )

    related_contacts = find_related_contacts(db, phone, email)

    if not related_contacts:
        return new_contact
    
    # if rlated contact exists
    # set the oldest as primary contact
    primary_contact = find_oldest_primary_contact(related_contacts)

    # update remaining contacts to be secondary and link to new primary
    update_to_secondary(db,primary_contact,related_contacts)

    db.commit()
    return primary_contact

    