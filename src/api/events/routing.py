from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from .models import (EventModel,
                     get_utc_now, 
                      EventBucketSchema, 
                      EventCreateSchema)
                      #EventUpdateSchema)
import os 
from api.db.session import get_session
from sqlmodel import Session, select
from sqlalchemy import func, case
from timescaledb.hyperfunctions import time_bucket
from datetime import datetime,timedelta, timezone


router = APIRouter()

from api.db.config import DATABASE_URL

# @router.get("/", response_model=EventListSchema)
# def read_events(session: Session = Depends(get_session)):
#     # query all data from the database
#     query = select(EventModel).order_by(EventModel.updated_at.desc()).limit(10)
#     results = session.exec(query).all()
#     return {"results": results, 
#             "count": len(results)}  # Example data, replace with actual logic

DEFAULT_LOOKUP_PAGES = [
        "/", "/about", "/pricing", "/contact", 
        "/blog", "/products", "/login", "/signup",
        "/dashboard", "/settings"
    ]

@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query(default="1 day"),
    pages: List = Query(default = None), 
    session: Session = Depends(get_session)):
    # a bunch of items in a table
    os_case = case(
        (EventModel.user_agent.ilike('%windows%'), 'Windows'),
        (EventModel.user_agent.ilike('%macintosh%'), 'MacOS'),
        (EventModel.user_agent.ilike('%iphone%'), 'iOS'),
        (EventModel.user_agent.ilike('%android%'), 'Android'),
        (EventModel.user_agent.ilike('%linux%'), 'Linux'),
        else_='Other'
    ).label('operating_system')
    # query all data from the database
    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    # start = datetime.now(timezone.utc) - timedelta(hours=1)
    # finish = datetime.now(timezone.utc) + timedelta(hours=1)
    query = (
        select(
            bucket.label('bucket'), 
            os_case, 
            EventModel.page.label('page'),
            func.avg(EventModel.duration).label('avg_duration'),
            func.count().label('count')
        )
        .where(
            # EventModel.time > start,
            # EventModel.time <= finish,
            EventModel.page.in_(lookup_pages)
        )
        .group_by(
            bucket, 
            os_case, 
            EventModel.page, 
        )
        .order_by(
            bucket, 
            os_case, 
            EventModel.page
        )
    )
    results = session.exec(query).fetchall()
    return results


@router.post("/", response_model = EventModel)
def create_event(
    payload : EventCreateSchema, 
    session: Session = Depends(get_session)) :
    
    data = payload.model_dump() # payload > dict > pydantic 
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

# @router.put("/{event_id}", response_model=EventModel)
# def update_event(event_id: int, 
#                  payload : EventUpdateSchema, 
#                  session: Session = Depends(get_session) ):
#     query = select(EventModel).where(EventModel.id == event_id)
#     obj = session.exec(query).first()
#     if not obj:
#         raise HTTPException(status_code=404, detail="Event not found")
#     data = payload.model_dump()
#     for key, value in data.items():
#         setattr(obj, key, value)
#     obj.updated_at = get_utc_now()
#     session.add(obj)
#     session.commit()
#     session.refresh(obj)
#     return obj
 


@router.get("/{event_id}", response_model=EventModel)
def read_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    results = session.exec(query).first()
    if not results:
        raise HTTPException(status_code=404, detail="Event not found")
    return results 