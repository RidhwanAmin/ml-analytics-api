#from pydantic import BaseModel, Field
from typing import List, Optional
from sqlmodel import Field, SQLModel, Field
import sqlmodel
from datetime import datetime, timezone
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now


# def get_utc_now(): 
#     return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

# page visits  at any given time 

class EventModel(TimescaleModel, table=True):
    #__tablename__ = "eventmodel"
    # id : Optional[int] = Field(default=None, primary_key=True)
    page : str = Field(index = True) # / about / contact # pricing 
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0) 

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"

class EventListSchema(SQLModel):
    results: List[EventModel]
    count : int

class EventBucketSchema(SQLModel):
    bucket : datetime
    page: str
    operating_system:  Optional[str] = ""
    avg_duration:  Optional[float] = 0.0
    count : int

class EventCreateSchema(SQLModel):
    page : str
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0) 

# class EventUpdateSchema(SQLModel):
#     description: str
    

