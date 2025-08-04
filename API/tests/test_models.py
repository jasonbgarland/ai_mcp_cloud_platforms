import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import sys
import os

# Add the parent directory to the path so we can import our models
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Base, Developer, CloudResource, Permission, CloudTypeEnum, PermissionEnum


class TestModels(unittest.TestCase):
    """Test suite for SQLAlchemy models"""
    
    def setUp(self):
        """Set up an in-memory SQLite database for testing"""
        self.engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def tearDown(self):
        """Clean up after each test"""
        self.session.close()
        Base.metadata.drop_all(self.engine)
    
    def test_developer_creation(self):
        """Test creating a developer"""
        dev = Developer(name="John Doe", email="john@example.com")
        self.session.add(dev)
        self.session.commit()
        
        assert dev.id is not None
        assert dev.name == "John Doe"
        assert dev.email == "john@example.com"
    
    def test_developer_unique_email(self):
        """Test that developer email must be unique"""
        dev1 = Developer(name="John Doe", email="john@example.com")
        dev2 = Developer(name="Jane Doe", email="john@example.com")
        
        self.session.add(dev1)
        self.session.commit()
        
        self.session.add(dev2)
        with self.assertRaises(IntegrityError):
            self.session.commit()
    
    def test_cloud_resource_creation(self):
        """Test creating a cloud resource"""
        resource = CloudResource(name="S3 Bucket", cloud_type=CloudTypeEnum.AWS)
        self.session.add(resource)
        self.session.commit()
        
        assert resource.id is not None
        assert resource.name == "S3 Bucket"
        assert resource.cloud_type == CloudTypeEnum.AWS
    
    def test_permission_creation(self):
        """Test creating a permission"""
        # Create developer and resource first
        dev = Developer(name="John Doe", email="john@example.com")
        resource = CloudResource(name="S3 Bucket", cloud_type=CloudTypeEnum.AWS)
        self.session.add_all([dev, resource])
        self.session.commit()
        
        # Create permission
        perm = Permission(
            developer_id=dev.id,
            resource_id=resource.id,
            permission=PermissionEnum.READ
        )
        self.session.add(perm)
        self.session.commit()
        
        assert perm.id is not None
        assert perm.developer_id == dev.id
        assert perm.resource_id == resource.id
        assert perm.permission == PermissionEnum.READ
    
    def test_permission_relationships(self):
        """Test permission relationships work correctly"""
        # Create developer and resource
        dev = Developer(name="John Doe", email="john@example.com")
        resource = CloudResource(name="S3 Bucket", cloud_type=CloudTypeEnum.AWS)
        self.session.add_all([dev, resource])
        self.session.commit()
        
        # Create permission
        perm = Permission(
            developer_id=dev.id,
            resource_id=resource.id,
            permission=PermissionEnum.WRITE
        )
        self.session.add(perm)
        self.session.commit()
        
        # Test relationships
        assert perm.developer == dev
        assert perm.cloud_resource == resource
        assert dev.permissions[0] == perm
        assert resource.permissions[0] == perm
    
    def test_multiple_permissions_same_developer(self):
        """Test that a developer can have multiple permissions"""
        dev = Developer(name="John Doe", email="john@example.com")
        resource1 = CloudResource(name="S3 Bucket", cloud_type=CloudTypeEnum.AWS)
        resource2 = CloudResource(name="Azure Blob", cloud_type=CloudTypeEnum.AZURE)
        self.session.add_all([dev, resource1, resource2])
        self.session.commit()
        
        perm1 = Permission(
            developer_id=dev.id,
            resource_id=resource1.id,
            permission=PermissionEnum.READ
        )
        perm2 = Permission(
            developer_id=dev.id,
            resource_id=resource2.id,
            permission=PermissionEnum.WRITE
        )
        self.session.add_all([perm1, perm2])
        self.session.commit()
        
        assert len(dev.permissions) == 2
        assert perm1 in dev.permissions
        assert perm2 in dev.permissions
    
    def test_multiple_permissions_same_resource(self):
        """Test that a resource can have multiple permissions (different developers)"""
        dev1 = Developer(name="John Doe", email="john@example.com")
        dev2 = Developer(name="Jane Doe", email="jane@example.com")
        resource = CloudResource(name="S3 Bucket", cloud_type=CloudTypeEnum.AWS)
        self.session.add_all([dev1, dev2, resource])
        self.session.commit()
        
        perm1 = Permission(
            developer_id=dev1.id,
            resource_id=resource.id,
            permission=PermissionEnum.READ
        )
        perm2 = Permission(
            developer_id=dev2.id,
            resource_id=resource.id,
            permission=PermissionEnum.WRITE
        )
        self.session.add_all([perm1, perm2])
        self.session.commit()
        
        assert len(resource.permissions) == 2
        assert perm1 in resource.permissions
        assert perm2 in resource.permissions
    
    def test_current_join_table_behavior(self):
        """Test the new property-based access to resources/developers"""
        dev = Developer(name="John Doe", email="john@example.com")
        resource = CloudResource(name="S3 Bucket", cloud_type=CloudTypeEnum.AWS)
        self.session.add_all([dev, resource])
        self.session.commit()
        
        # Create permission to establish relationship
        perm = Permission(
            developer_id=dev.id,
            resource_id=resource.id,
            permission=PermissionEnum.READ
        )
        self.session.add(perm)
        self.session.commit()
        
        # Test the new property-based access
        self.assertIn(resource, dev.cloud_resources)
        self.assertIn(dev, resource.developers)
        self.assertEqual(dev.get_permission_for_resource(resource.id), PermissionEnum.READ)
        self.assertEqual(resource.get_permission_for_developer(dev.id), PermissionEnum.READ)
    
    def test_duplicate_permission_should_fail_with_unique_constraint(self):
        """Test that duplicate permissions fail with unique constraint"""
        dev = Developer(name="John Doe", email="john@example.com")
        resource = CloudResource(name="S3 Bucket", cloud_type=CloudTypeEnum.AWS)
        self.session.add_all([dev, resource])
        self.session.commit()
        
        perm1 = Permission(
            developer_id=dev.id,
            resource_id=resource.id,
            permission=PermissionEnum.READ
        )
        perm2 = Permission(
            developer_id=dev.id,
            resource_id=resource.id,
            permission=PermissionEnum.WRITE
        )
        
        self.session.add(perm1)
        self.session.commit()
        
        self.session.add(perm2)
        # This should now fail with unique constraint
        with self.assertRaises(IntegrityError):
            self.session.commit()
    
    def test_helper_methods(self):
        """Test the helper methods for getting permissions"""
        dev = Developer(name="John Doe", email="john@example.com")
        resource1 = CloudResource(name="S3 Bucket", cloud_type=CloudTypeEnum.AWS)
        resource2 = CloudResource(name="Azure Blob", cloud_type=CloudTypeEnum.AZURE)
        self.session.add_all([dev, resource1, resource2])
        self.session.commit()
        
        perm1 = Permission(
            developer_id=dev.id,
            resource_id=resource1.id,
            permission=PermissionEnum.READ
        )
        perm2 = Permission(
            developer_id=dev.id,
            resource_id=resource2.id,
            permission=PermissionEnum.WRITE
        )
        self.session.add_all([perm1, perm2])
        self.session.commit()
        
        # Test developer helper methods
        self.assertEqual(len(dev.cloud_resources), 2)
        self.assertEqual(dev.get_permission_for_resource(resource1.id), PermissionEnum.READ)
        self.assertEqual(dev.get_permission_for_resource(resource2.id), PermissionEnum.WRITE)
        self.assertIsNone(dev.get_permission_for_resource(999))  # Non-existent resource
        
        # Test resource helper methods
        self.assertEqual(len(resource1.developers), 1)
        self.assertEqual(resource1.get_permission_for_developer(dev.id), PermissionEnum.READ)
        self.assertIsNone(resource1.get_permission_for_developer(999))  # Non-existent developer


if __name__ == "__main__":
    unittest.main()
