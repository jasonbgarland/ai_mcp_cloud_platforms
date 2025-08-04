#!/usr/bin/env python3
"""
Test script for enhanced API routes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models import Base, CloudTypeEnum, PermissionEnum
from db import get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class TestEnhancedAPI(unittest.TestCase):
    
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)
        
    def tearDown(self):
        Base.metadata.drop_all(bind=engine)
    
    def test_developer_crud(self):
        """Test developer CRUD operations"""
        # Create developer
        response = self.client.post("/developers/", json={
            "name": "John Doe",
            "email": "john@example.com"
        })
        self.assertEqual(response.status_code, 200)
        developer_data = response.json()
        self.assertEqual(developer_data["name"], "John Doe")
        self.assertEqual(developer_data["email"], "john@example.com")
        developer_id = developer_data["id"]
        
        # Get developer
        response = self.client.get(f"/developers/{developer_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "John Doe")
        
        # Update developer
        response = self.client.put(f"/developers/{developer_id}", json={
            "name": "John Updated",
            "email": "john.updated@example.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "John Updated")
        
        # List developers
        response = self.client.get("/developers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        
        # Delete developer
        response = self.client.delete(f"/developers/{developer_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["ok"], True)
    
    def test_cloud_resource_crud(self):
        """Test cloud resource CRUD operations"""
        # Create resource
        response = self.client.post("/cloud_resources/", json={
            "name": "S3 Bucket",
            "cloud_type": "AWS"
        })
        self.assertEqual(response.status_code, 200)
        resource_data = response.json()
        self.assertEqual(resource_data["name"], "S3 Bucket")
        self.assertEqual(resource_data["cloud_type"], "AWS")
        resource_id = resource_data["id"]
        
        # Get resource
        response = self.client.get(f"/cloud_resources/{resource_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "S3 Bucket")
        
        # Update resource
        response = self.client.put(f"/cloud_resources/{resource_id}", json={
            "name": "Updated S3 Bucket",
            "cloud_type": "AWS"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated S3 Bucket")
        
        # List resources
        response = self.client.get("/cloud_resources/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        
        # Delete resource
        response = self.client.delete(f"/cloud_resources/{resource_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["ok"], True)
    
    def test_permission_crud_and_filtering(self):
        """Test permission CRUD and filtering operations"""
        # Create developer and resource first
        dev_response = self.client.post("/developers/", json={
            "name": "John Doe",
            "email": "john@example.com"
        })
        developer_id = dev_response.json()["id"]
        
        resource_response = self.client.post("/cloud_resources/", json={
            "name": "S3 Bucket",
            "cloud_type": "AWS"
        })
        resource_id = resource_response.json()["id"]
        
        # Create permission
        response = self.client.post("/permissions/", json={
            "developer_id": developer_id,
            "resource_id": resource_id,
            "permission": "READ"
        })
        self.assertEqual(response.status_code, 200)
        permission_data = response.json()
        self.assertEqual(permission_data["permission"], "READ")
        permission_id = permission_data["id"]
        
        # Test duplicate permission fails
        response = self.client.post("/permissions/", json={
            "developer_id": developer_id,
            "resource_id": resource_id,
            "permission": "WRITE"
        })
        self.assertEqual(response.status_code, 400)
        
        # Get permission
        response = self.client.get(f"/permissions/{permission_id}")
        self.assertEqual(response.status_code, 200)
        
        # Update permission
        response = self.client.put(f"/permissions/{permission_id}", json={
            "developer_id": developer_id,
            "resource_id": resource_id,
            "permission": "RW"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["permission"], "RW")
        
        # Filter permissions by developer
        response = self.client.get(f"/permissions/?developer_id={developer_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        
        # Filter permissions by resource
        response = self.client.get(f"/permissions/?resource_id={resource_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        
        # Get permissions by developer endpoint
        response = self.client.get(f"/permissions/by-developer/{developer_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        
        # Get permissions by resource endpoint
        response = self.client.get(f"/permissions/by-resource/{resource_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        
        # Delete permission
        response = self.client.delete(f"/permissions/{permission_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["ok"], True)
    
    def test_detailed_views(self):
        """Test detailed views with relationships"""
        # Create developer and resource
        dev_response = self.client.post("/developers/", json={
            "name": "John Doe",
            "email": "john@example.com"
        })
        developer_id = dev_response.json()["id"]
        
        resource_response = self.client.post("/cloud_resources/", json={
            "name": "S3 Bucket",
            "cloud_type": "AWS"
        })
        resource_id = resource_response.json()["id"]
        
        # Create permission
        self.client.post("/permissions/", json={
            "developer_id": developer_id,
            "resource_id": resource_id,
            "permission": "READ"
        })
        
        # Test developer detailed view
        response = self.client.get(f"/developers/{developer_id}/detailed")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "John Doe")
        self.assertEqual(len(data["permissions"]), 1)
        
        # Test resource detailed view
        response = self.client.get(f"/cloud_resources/{resource_id}/detailed")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "S3 Bucket")
        self.assertEqual(len(data["permissions"]), 1)


if __name__ == "__main__":
    unittest.main()
