from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/rewards", tags=["Rewards"])


@router.post("/", response_model=schemas.RewardOut, status_code=status.HTTP_201_CREATED)
def create_reward(reward: schemas.RewardCreate, db: Session = Depends(get_db)):
    # Fixed: Replaced deprecated `.dict()` with `.model_dump()` & removed hidden spaces
    new_reward = models.Reward(**reward.model_dump())
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)
    return new_reward


@router.get("/", response_model=list[schemas.RewardOut])
def get_rewards(db: Session = Depends(get_db)):
    return db.query(models.Reward).all()


@router.delete("/{reward_id}")
def delete_reward(reward_id: int, db: Session = Depends(get_db)):
    reward = db.query(models.Reward).filter(models.Reward.id == reward_id).first()

    if not reward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found"
        )

    db.delete(reward)
    db.commit()
    return {"message": "Reward deleted"}
