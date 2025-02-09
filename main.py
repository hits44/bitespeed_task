from fastapi import FastAPI , Depends
from database import get_db, Base, engine

from sqlalchemy.orm import Session

# import models and init tables 
from models import Contact
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/identify")
def identify_contact(phoneNumber : str = None, email: str = None, db: Session = Depends(get_db)):
    pass