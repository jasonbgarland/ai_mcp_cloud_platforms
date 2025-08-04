#!/usr/bin/env python3
"""
Simple manual test for API functionality
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Enhanced API Routes...")
    
    # Test 1: Create Developer
    print("\n1️⃣ Creating developer...")
    dev_data = {
        "name": "Test Developer",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/developers/", json=dev_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        developer = response.json()
        developer_id = developer["id"]
        print(f"✅ Created developer: {developer['name']} (ID: {developer_id})")
    else:
        print(f"❌ Failed: {response.text}")
        return
    
    # Test 2: Create Cloud Resource
    print("\n2️⃣ Creating cloud resource...")
    resource_data = {
        "name": "Test S3 Bucket",
        "cloud_type": "AWS"
    }
    response = requests.post(f"{BASE_URL}/cloud_resources/", json=resource_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        resource = response.json()
        resource_id = resource["id"]
        print(f"✅ Created resource: {resource['name']} (ID: {resource_id})")
    else:
        print(f"❌ Failed: {response.text}")
        return
    
    # Test 3: Create Permission
    print("\n3️⃣ Creating permission...")
    perm_data = {
        "developer_id": developer_id,
        "resource_id": resource_id,
        "permission": "READ"
    }
    response = requests.post(f"{BASE_URL}/permissions/", json=perm_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        permission = response.json()
        permission_id = permission["id"]
        print(f"✅ Created permission: {permission['permission']} (ID: {permission_id})")
    else:
        print(f"❌ Failed: {response.text}")
        return
    
    # Test 4: Test Unique Constraint
    print("\n4️⃣ Testing unique constraint...")
    duplicate_perm = {
        "developer_id": developer_id,
        "resource_id": resource_id,
        "permission": "WRITE"
    }
    response = requests.post(f"{BASE_URL}/permissions/", json=duplicate_perm)
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print("✅ Unique constraint working - duplicate permission rejected")
    else:
        print(f"❌ Expected 400, got {response.status_code}: {response.text}")
    
    # Test 5: Filter Permissions by Developer
    print("\n5️⃣ Testing permission filtering by developer...")
    response = requests.get(f"{BASE_URL}/permissions/?developer_id={developer_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        permissions = response.json()
        print(f"✅ Found {len(permissions)} permission(s) for developer {developer_id}")
    else:
        print(f"❌ Failed: {response.text}")
    
    # Test 6: Get Developer with Resources
    print("\n6️⃣ Testing detailed developer view...")
    response = requests.get(f"{BASE_URL}/developers/{developer_id}/detailed")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        detailed_dev = response.json()
        print(f"✅ Developer {detailed_dev['name']} has {len(detailed_dev['permissions'])} permission(s)")
    else:
        print(f"❌ Failed: {response.text}")
    
    # Test 7: Get Resource with Developers
    print("\n7️⃣ Testing detailed resource view...")
    response = requests.get(f"{BASE_URL}/cloud_resources/{resource_id}/detailed")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        detailed_resource = response.json()
        print(f"✅ Resource {detailed_resource['name']} has {len(detailed_resource['permissions'])} permission(s)")
    else:
        print(f"❌ Failed: {response.text}")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
