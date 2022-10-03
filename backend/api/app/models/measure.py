from sqlalchemy import table
from sqlmodel import Field, SQLModel
from typing import Optional

class Measure(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)