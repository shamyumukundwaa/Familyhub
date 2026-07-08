from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/chores", tags=["Chores"])


@router.post("/", response_model=schemas.ChoreOut, status_code=status.HTTP_201_CREATED)
def create_chore(chore: schemas.ChoreCreate, db: Session = Depends(get_db)):
    # Validate that the child actually exists before creating the chore
    child_exists = (
        db.query(models.User).filter(models.User.id == chore.assigned_to).first()
    )
    if not child_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned child user not found",
        )

    new_chore = models.Chore(**chore.model_dump())
    db.add(new_chore)
    db.commit()
    db.refresh(new_chore)
    return new_chore


@router.get("/child/{child_id}", response_model=list[schemas.ChoreOut])
def get_child_chores(child_id: int, db: Session = Depends(get_db)):
    chores = db.query(models.Chore).filter(models.Chore.assigned_to == child_id).all()
    return chores


@router.get("/", response_model=list[schemas.ChoreOut])
def get_all_chores(db: Session = Depends(get_db)):
    return db.query(models.Chore).all()


@router.patch("/{chore_id}/complete")
def complete_chore(chore_id: int, db: Session = Depends(get_db)):
    chore = db.query(models.Chore).filter(models.Chore.id == chore_id).first()

    if not chore:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chore not found"
        )
    if chore.status == "done":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Chore already completed"
        )

    child = db.query(models.User).filter(models.User.id == chore.assigned_to).first()

    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The child assigned to this chore no longer exists",
        )

    chore.status = "done"
    child.points += chore.points_value

    db.commit()
    db.refresh(child) 
    return {
        "message": "Chore completed!",
        "points_earned": chore.points_value,
        "total_points": child.points,
    }


@router.delete("/{chore_id}")
def delete_chore(chore_id: int, db: Session = Depends(get_db)):
    chore = db.query(models.Chore).filter(models.Chore.id == chore_id).first()
    if not chore:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chore not found"
        )

    db.delete(chore)
    db.commit()
    return {"message": "Chore deleted"}
