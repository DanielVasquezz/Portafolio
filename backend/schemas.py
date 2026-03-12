from pydantic import BaseModel, EmailStr

from typing import Optional

from datetime import datetime


class ContactCreate(BaseModel):
    name: str

    email: EmailStr

    message: str

class ContactResponse(ContactCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

