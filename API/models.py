import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CloudTypeEnum(enum.Enum):
    AWS = "AWS"
    AZURE = "AZURE"
    GCP = "GCP"

class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    @property
    def cloud_resources(self):
        """Get all cloud resources this developer has permissions for"""
        return [perm.cloud_resource for perm in self.permissions]
    
    def get_permission_for_resource(self, resource_id):
        """Get the permission level for a specific resource"""
        for perm in self.permissions:
            if perm.resource_id == resource_id:
                return perm.permission
        return None

class CloudResource(Base):
    __tablename__ = "cloud_resources"

    id = Column(Integer, primary_key=True, index=True)
    cloud_type = Column(Enum(CloudTypeEnum), nullable=False)
    name = Column(String, nullable=False)
    
    @property
    def developers(self):
        """Get all developers who have permissions for this resource"""
        return [perm.developer for perm in self.permissions]
    
    def get_permission_for_developer(self, developer_id):
        """Get the permission level for a specific developer"""
        for perm in self.permissions:
            if perm.developer_id == developer_id:
                return perm.permission
        return None

class PermissionEnum(enum.Enum):
    READ = "READ"
    WRITE = "WRITE"
    RW = "RW"

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = (
        UniqueConstraint('developer_id', 'resource_id', name='_developer_resource_uc'),
    )

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("cloud_resources.id"), nullable=False)
    developer_id = Column(Integer, ForeignKey("developers.id"), nullable=False)
    permission = Column(Enum(PermissionEnum), nullable=False)

    developer = relationship("Developer", back_populates="permissions")
    cloud_resource = relationship("CloudResource", back_populates="permissions")

# Add the back_populates to complete the relationships
Developer.permissions = relationship("Permission", back_populates="developer")
CloudResource.permissions = relationship("Permission", back_populates="cloud_resource")
