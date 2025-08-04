import enum
from typing import List

from pydantic import BaseModel, EmailStr


class CloudTypeEnum(str, enum.Enum):
    AWS = "AWS"
    AZURE = "AZURE"
    GCP = "GCP"

class PermissionEnum(str, enum.Enum):
    READ = "READ"
    WRITE = "WRITE"
    RW = "RW"

# Base schemas without relationships to avoid circular imports
class DeveloperBase(BaseModel):
    name: str
    email: EmailStr

class DeveloperCreate(DeveloperBase):
    pass

class DeveloperRead(DeveloperBase):
    id: int
    class Config:
        from_attributes = True

class CloudResourceBase(BaseModel):
    name: str
    cloud_type: CloudTypeEnum

class CloudResourceCreate(CloudResourceBase):
    pass

class CloudResourceRead(CloudResourceBase):
    id: int
    class Config:
        from_attributes = True

class PermissionBase(BaseModel):
    resource_id: int
    developer_id: int
    permission: PermissionEnum

class PermissionCreate(PermissionBase):
    pass

class PermissionRead(PermissionBase):
    id: int
    class Config:
        from_attributes = True

# Extended schemas with relationships for detailed views
class PermissionWithDeveloper(PermissionRead):
    developer: DeveloperRead

class PermissionWithResource(PermissionRead):
    cloud_resource: CloudResourceRead

class PermissionWithBoth(PermissionRead):
    developer: DeveloperRead
    cloud_resource: CloudResourceRead

class DeveloperWithResources(DeveloperRead):
    permissions: List[PermissionWithResource] = []

class CloudResourceWithDevelopers(CloudResourceRead):
    permissions: List[PermissionWithDeveloper] = []
