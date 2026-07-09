from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/requests", tags=["Permission Requests"])


@router.post(
    "/", response_model=schemas.RequestOut, status_code=status.HTTP_201_CREATED
)
def create_request(req: schemas.RequestCreate, db: Session = Depends(get_db)):
    child_exists = db.query(models.User).filter(models.User.id == req.child_id).first()
    if not child_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Child user not found"
        )

    new_req = models.PermissionRequest(**req.model_dump())
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req


@router.get("/pending", response_model=list[schemas.RequestOut])
def get_pending(db: Session = Depends(get_db)):
    return (
        db.query(models.PermissionRequest)
        .filter(models.PermissionRequest.status == "pending")
        .all()
    )


@router.get("/child/{child_id}", response_model=list[schemas.RequestOut])
def get_child_requests(child_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.PermissionRequest)
        .filter(models.PermissionRequest.child_id == child_id)
        .all()
    )


@router.patch("/{req_id}/decision")
def respond_to_request(
    req_id: int,
    action: str = Query(..., description="Must be 'approved' or 'denied'"),
    db: Session = Depends(get_db),
):
    if action not in ["approved", "denied"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action must be 'approved' or 'denied'",
        )

    req = (
        db.query(models.PermissionRequest)
        .filter(models.PermissionRequest.id == req_id)
        .first()
    )

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Request not found"
        )

    req.status = action
    db.commit()
    return {"message": f"Request {action}"}
