from typing import List

from db import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import CloudResource
from schemas import CloudResourceCreate, CloudResourceRead, CloudResourceWithDevelopers
from sqlalchemy.orm import Session

router = APIRouter(prefix="/cloud_resources", tags=["cloud_resources"])

@router.post("/", response_model=CloudResourceRead)
def create_cloud_resource(resource: CloudResourceCreate, db: Session = Depends(get_db)):
    db_resource = CloudResource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.get("/", response_model=List[CloudResourceRead])
def list_cloud_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(CloudResource).offset(skip).limit(limit).all()

@router.get("/{resource_id}", response_model=CloudResourceRead)
def get_cloud_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(CloudResource).filter(CloudResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="CloudResource not found")
    return resource

@router.get("/{resource_id}/detailed", response_model=CloudResourceWithDevelopers)
def get_cloud_resource_with_developers(resource_id: int, db: Session = Depends(get_db)):
    """Get cloud resource with all developer permissions"""
    resource = db.query(CloudResource).filter(CloudResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="CloudResource not found")
    return resource

@router.put("/{resource_id}", response_model=CloudResourceRead)
def update_cloud_resource(resource_id: int, resource: CloudResourceCreate, db: Session = Depends(get_db)):
    db_resource = db.query(CloudResource).filter(CloudResource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="CloudResource not found")
    for key, value in resource.dict().items():
        setattr(db_resource, key, value)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.delete("/{resource_id}", response_model=dict)
def delete_cloud_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = db.query(CloudResource).filter(CloudResource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="CloudResource not found")
    db.delete(db_resource)
    db.commit()
    return {"ok": True}
