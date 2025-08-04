from typing import List

from db import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import Developer
from schemas import DeveloperCreate, DeveloperRead, DeveloperWithResources
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/developers", tags=["developer"])

@router.post("/", response_model=DeveloperRead)
def create_developer(developer: DeveloperCreate, db: Session = Depends(get_db)):
    db_dev = Developer(name=developer.name, email=developer.email)
    db.add(db_dev)
    try:
        db.commit()
        db.refresh(db_dev)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Developer with this email already exists.")
    return db_dev

@router.get("/", response_model=List[DeveloperRead])
def list_developers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Developer).offset(skip).limit(limit).all()

@router.get("/{developer_id}", response_model=DeveloperRead)
def get_developer(developer_id: int, db: Session = Depends(get_db)):
    dev = db.query(Developer).filter(Developer.id == developer_id).first()
    if not dev:
        raise HTTPException(status_code=404, detail="Developer not found")
    return dev

@router.get("/{developer_id}/detailed", response_model=DeveloperWithResources)
def get_developer_with_resources(developer_id: int, db: Session = Depends(get_db)):
    """Get developer with all their resource permissions"""
    dev = db.query(Developer).filter(Developer.id == developer_id).first()
    if not dev:
        raise HTTPException(status_code=404, detail="Developer not found")
    return dev

@router.put("/{developer_id}", response_model=DeveloperRead)
def update_developer(developer_id: int, developer: DeveloperCreate, db: Session = Depends(get_db)):
    db_dev = db.query(Developer).filter(Developer.id == developer_id).first()
    if not db_dev:
        raise HTTPException(status_code=404, detail="Developer not found")
    db_dev.name = developer.name
    db_dev.email = developer.email
    try:
        db.commit()
        db.refresh(db_dev)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Developer with this email already exists.")
    return db_dev

@router.delete("/{developer_id}", response_model=dict)
def delete_developer(developer_id: int, db: Session = Depends(get_db)):
    db_dev = db.query(Developer).filter(Developer.id == developer_id).first()
    if not db_dev:
        raise HTTPException(status_code=404, detail="Developer not found")
    db.delete(db_dev)
    db.commit()
    return {"ok": True}
