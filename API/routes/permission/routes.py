from typing import List, Optional

from db import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import Permission, Developer, CloudResource
from schemas import (
    PermissionCreate, 
    PermissionRead, 
    PermissionWithDeveloper,
    PermissionWithResource
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.post("/", response_model=PermissionRead)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    # Verify developer and resource exist
    developer = db.query(Developer).filter(Developer.id == permission.developer_id).first()
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    
    resource = db.query(CloudResource).filter(CloudResource.id == permission.resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="CloudResource not found")
    
    db_permission = Permission(**permission.dict())
    db.add(db_permission)
    try:
        db.commit()
        db.refresh(db_permission)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail=f"Permission already exists for developer {permission.developer_id} and resource {permission.resource_id}"
        )
    return db_permission

@router.get("/", response_model=List[PermissionRead])
def list_permissions(
    skip: int = 0, 
    limit: int = 100, 
    developer_id: Optional[int] = None,
    resource_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get permissions with optional filtering by developer_id or resource_id"""
    query = db.query(Permission)
    
    if developer_id is not None:
        query = query.filter(Permission.developer_id == developer_id)
    
    if resource_id is not None:
        query = query.filter(Permission.resource_id == resource_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/by-developer/{developer_id}", response_model=List[PermissionWithResource])
def get_permissions_by_developer(developer_id: int, db: Session = Depends(get_db)):
    """Get all permissions for a specific developer with resource details"""
    developer = db.query(Developer).filter(Developer.id == developer_id).first()
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    
    permissions = db.query(Permission).filter(Permission.developer_id == developer_id).all()
    return permissions

@router.get("/by-resource/{resource_id}", response_model=List[PermissionWithDeveloper])
def get_permissions_by_resource(resource_id: int, db: Session = Depends(get_db)):
    """Get all permissions for a specific resource with developer details"""
    resource = db.query(CloudResource).filter(CloudResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="CloudResource not found")
    
    permissions = db.query(Permission).filter(Permission.resource_id == resource_id).all()
    return permissions

@router.get("/{permission_id}", response_model=PermissionRead)
def get_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

@router.put("/{permission_id}", response_model=PermissionRead)
def update_permission(permission_id: int, permission: PermissionCreate, db: Session = Depends(get_db)):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    # Verify developer and resource exist if they're being changed
    if permission.developer_id != db_permission.developer_id:
        developer = db.query(Developer).filter(Developer.id == permission.developer_id).first()
        if not developer:
            raise HTTPException(status_code=404, detail="Developer not found")
    
    if permission.resource_id != db_permission.resource_id:
        resource = db.query(CloudResource).filter(CloudResource.id == permission.resource_id).first()
        if not resource:
            raise HTTPException(status_code=404, detail="CloudResource not found")
    
    for key, value in permission.dict().items():
        setattr(db_permission, key, value)
    
    try:
        db.commit()
        db.refresh(db_permission)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail=f"Permission already exists for developer {permission.developer_id} and resource {permission.resource_id}"
        )
    return db_permission

@router.delete("/{permission_id}", response_model=dict)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(db_permission)
    db.commit()
    return {"ok": True}
