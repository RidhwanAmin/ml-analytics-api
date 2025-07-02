from pydantic import BaseModel, Field
from typing import List, Optional

class EventSchema(BaseModel):
    id: int
    page : Optional[str] = None
    description: Optional[str] = None 

class EventListSchema(BaseModel):
    results: List[EventSchema]
    count : int

class EventCreateSchema(BaseModel):
    page : str
    description: Optional[str] = Field(default="Description of the event") 

class EventUpdateSchema(BaseModel):
    description: str
    

