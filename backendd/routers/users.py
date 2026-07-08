from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/family", response_model=list[schemas.UserOut])
def get_family(db: Session = Depends(get_db)):
    children = db.query(models.User).filter(models.User.role == "child").all()
    return children



@router.get("/family/progress")
def get_family_progress(db: Session = Depends(get_db)):
    children = db.query(models.User).filter(models.User.role == "child").all()

    result = []
    for child in children:
        total = len(child.chores)
        done = sum(1 for c in child.chores if c.status == "done")
        progress = round((done / total) * 100) if total > 0 else 0
        result.append(
            {
                "id": child.id,
                "name": child.name,
                "points": child.points,
                "chore_progress": progress,
            }
        )
    return result



@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
