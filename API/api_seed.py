#!/usr/bin/env python3
"""
API-based seeding script for the MCP demo database.
Creates developers, cloud resources, and their relationships via API calls.
"""

import os
import random
import time

import requests

# API base URL
API_BASE = os.getenv("API_URL", "http://localhost:8000")

def wait_for_api():
    """Wait for API to be ready"""
    for i in range(30):
        try:
            response = requests.get(f"{API_BASE}/", timeout=5)  # Use root endpoint first
            if response.status_code == 200:
                print("API is ready!")
                return
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        print(f"Waiting for API... ({i+1}/30)")
        time.sleep(2)
    raise Exception("API not available after 60 seconds")

def create_developers():
    """Create 5 developers via API"""
    developers = [
        {"name": "Alice Smith", "email": "alice@example.com"},
        {"name": "Bob Jones", "email": "bob@example.com"},
        {"name": "Carol Lee", "email": "carol@example.com"},
        {"name": "David Kim", "email": "david@example.com"},
        {"name": "Eva Brown", "email": "eva@example.com"},
    ]
    
    created_devs = []
    for dev_data in developers:
        response = requests.post(f"{API_BASE}/developers/", json=dev_data)
        print(f"Developer creation status: {response.status_code}")
        if response.status_code in [200, 201]:
            created_devs.append(response.json())
            print(f"Created developer: {dev_data['name']}")
        else:
            print(f"Failed to create developer {dev_data['name']} (status {response.status_code}): {response.text}")
    
    return created_devs

def create_cloud_resources():
    """Create cloud resources via API"""
    cloud_types = ["AWS", "AZURE", "GCP"]
    resource_names = {
        "AWS": ["S3 Bucket", "EC2 Instance", "RDS DB", "Lambda Function", "DynamoDB Table"],
        "AZURE": ["VM", "Blob Storage", "SQL Database", "App Service", "Cosmos DB"],
        "GCP": ["BigQuery", "Compute Engine", "Cloud Storage", "Cloud SQL", "Pub/Sub"]
    }
    
    all_resources = []
    for cloud in cloud_types:
        for name in resource_names[cloud]:
            resource_data = {
                "name": f"{cloud} {name}",
                "cloud_type": cloud
            }
            response = requests.post(f"{API_BASE}/cloud_resources/", json=resource_data)
            if response.status_code in [200, 201]:
                all_resources.append(response.json())
                print(f"Created resource: {resource_data['name']}")
            else:
                print(f"Failed to create resource {resource_data['name']} (status {response.status_code}): {response.text}")
    
    return all_resources

def assign_resources_to_developers(developers, resources):
    """Assign 2-5 resources per cloud to each developer"""
    resources_by_cloud = {}
    for resource in resources:
        cloud = resource["cloud_type"]
        if cloud not in resources_by_cloud:
            resources_by_cloud[cloud] = []
        resources_by_cloud[cloud].append(resource)
    
    assignments = []
    permission_choices = ["READ", "WRITE", "RW"]
    
    for dev in developers:
        print(f"Assigning resources to {dev['name']}...")
        for cloud, cloud_resources in resources_by_cloud.items():
            # Assign 2-5 resources from this cloud to this developer
            num_resources = random.randint(2, min(5, len(cloud_resources)))
            assigned_resources = random.sample(cloud_resources, num_resources)
            
            for resource in assigned_resources:
                # Create permission record (which should also create the link)
                permission_data = {
                    "resource_id": resource["id"],
                    "developer_id": dev["id"],
                    "permission": random.choice(permission_choices)
                }
                
                response = requests.post(f"{API_BASE}/permissions/", json=permission_data)
                if response.status_code in [200, 201]:
                    assignments.append(response.json())
                    print(f"  Assigned {resource['name']} with {permission_data['permission']} permission")
                else:
                    print(f"  Failed to assign {resource['name']} (status {response.status_code}): {response.text}")
    
    return assignments

def main():
    """Main seeding function"""
    print("🌱 Starting API-based database seeding...")
    
    # Wait for API to be ready
    wait_for_api()
    
    # Create developers
    print("\n1️⃣ Creating developers...")
    developers = create_developers()
    
    # Create cloud resources
    print("\n2️⃣ Creating cloud resources...")
    resources = create_cloud_resources()
    
    # Assign resources to developers
    print("\n3️⃣ Assigning resources to developers...")
    assignments = assign_resources_to_developers(developers, resources)
    
    print("\n🎉 Seeding completed!")
    print(f"✅ Created {len(developers)} developers")
    print(f"✅ Created {len(resources)} cloud resources")
    print(f"✅ Created {len(assignments)} resource assignments")
    
    # Summary by cloud type
    cloud_counts = {}
    for assignment in assignments:
        # Get the resource to find its cloud type
        for resource in resources:
            if resource["id"] == assignment.get("resource_id"):
                cloud = resource["cloud_type"]
                cloud_counts[cloud] = cloud_counts.get(cloud, 0) + 1
                break
    
    print("\n📊 Assignment Summary by Cloud:")
    for cloud, count in sorted(cloud_counts.items()):
        print(f"   {cloud}: {count} assignments")
    
    print(f"\n💡 You can now test the MCP tools with developer IDs 1-{len(developers)} and resource IDs 1-{len(resources)}")

if __name__ == "__main__":
    main()
