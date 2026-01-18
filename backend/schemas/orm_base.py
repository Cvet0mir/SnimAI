from pydantic import BaseModel

class BaseORM(BaseModel):
    class Config:
        orm_mode = True
