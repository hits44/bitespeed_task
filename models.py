from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum

from database import Base

class Contact(Base):
    """Create Contact model which defines the entry in DB."""
    __tablename__="contacts"

    id = Column(Integer, primary_key=True )