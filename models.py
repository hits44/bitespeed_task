from sqlalchemy import Enum, Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base
# from enum import Enum
from datetime import datetime

class LinkPrecedenceEnum(Enum):
    primary="primary"
    secondary="secondary"

class Contact(Base):
    """Create Contact model which defines the entry in DB."""
    __tablename__="contacts"

    id = Column(Integer, primary_key=True)
    # set index at phonenumber and email 
    phoneNumber = Column(String, index=True)
    email = Column(String, index=True)

    # linkedId is id of a primary contact
    linkedId = Column(Integer, ForeignKey("contacts.id"))

    linkPrecedence = Column(Enum(
            'primary', 
            'secondary',
            name='link_precedence_enum'  # This creates the type in the database
        ), default=LinkPrecedenceEnum.primary, nullable=False)

    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt  = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    deletedAt = Column(DateTime)

    # populate primary  
    primary_contact = relationship("Contact", remote_side=[id], uselist=False, back_populates="secondary_contacts")

    # use lazy loading for large secondary contacts
    secondary_contacts =relationship("Contact", back_populates="primary_contact", foreign_keys=[linkedId], lazy="dynamic")

# print(LinkPrecedenceEnum.primary)