from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, timedelta
from database import get_db
import models, schemas

router = APIRouter(prefix="/events", tags=["Calendar"])


@router.post("/", response_model=schemas.EventOut, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    new_event = models.Event(**event.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.get("/today", response_model=list[schemas.EventOut])
def get_today_events(db: Session = Depends(get_db)):
    today = date.today()
    events = db.query(models.Event).filter(models.Event.date == today).all()
    return events


@router.get("/upcoming", response_model=list[schemas.EventOut])
def get_upcoming(db: Session = Depends(get_db)):
    
    today = date.today()
    next_week = today + timedelta(days=7)

    events = (
        db.query(models.Event)
        .filter(models.Event.date >= today, models.Event.date <= next_week)
        .all()
    )
    return events


@router.get("/", response_model=list[schemas.EventOut])
def get_all_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}
