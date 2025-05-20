from pydantic import BaseModel, Field
from datetime import date


class Identity(BaseModel):
    identity_number: str = Field(min_length=10, max_length=12)  # 11 digit id number
    surname: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=50)
    birth_date: date

    class Config:
        orm_mode = True


class IdentityCardRequest(Identity):
    pass


class IdentityCardResponse(Identity):
    id: int
    created_at: date
