import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'API')))

from models import (
    Base,
    CloudResource,
    CloudTypeEnum,
    Developer,
    Permission,
    PermissionEnum,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = os.getenv("POSTGRES_USER", "itadmin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password1234")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "demo_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed():

    import random
    session = SessionLocal()
    # Developers
    devs = [
        Developer(name="Alice Smith", email="alice@example.com"),
        Developer(name="Bob Jones", email="bob@example.com"),
        Developer(name="Carol Lee", email="carol@example.com"),
        Developer(name="David Kim", email="david@example.com"),
        Developer(name="Eva Brown", email="eva@example.com"),
    ]
    session.add_all(devs)
    session.commit()

    # Cloud types
    cloud_types = [CloudTypeEnum.AWS, CloudTypeEnum.AZURE, CloudTypeEnum.GCP]
    resource_names = {
        CloudTypeEnum.AWS: ["S3 Bucket", "EC2 Instance", "RDS DB", "Lambda Function", "DynamoDB Table"],
        CloudTypeEnum.AZURE: ["VM", "Blob Storage", "SQL Database", "App Service", "Cosmos DB"],
        CloudTypeEnum.GCP: ["BigQuery", "Compute Engine", "Cloud Storage", "Cloud SQL", "Pub/Sub"]
    }

    # First create all cloud resources (not tied to specific developers initially)
    all_resources = []
    for cloud in cloud_types:
        for name in resource_names[cloud]:
            res = CloudResource(name=f"{cloud.value} {name}", cloud_type=cloud)
            session.add(res)
            all_resources.append(res)
    session.commit()

    # Now assign permissions for developers to resources
    perm_choices = [PermissionEnum.READ, PermissionEnum.WRITE, PermissionEnum.RW]
    
    # For each developer, assign them to 2-5 random resources from each cloud type
    for dev in devs:
        for cloud in cloud_types:
            # Get resources for this cloud type
            cloud_resources = [r for r in all_resources if r.cloud_type == cloud]
            num_resources = random.randint(2, min(5, len(cloud_resources)))
            chosen_resources = random.sample(cloud_resources, num_resources)
            
            for res in chosen_resources:
                # Check if permission already exists for this dev-resource pair
                existing = session.query(Permission).filter_by(
                    developer_id=dev.id, 
                    resource_id=res.id
                ).first()
                
                if not existing:
                    perm = Permission(
                        resource_id=res.id,
                        developer_id=dev.id,
                        permission=random.choice(perm_choices)
                    )
                    session.add(perm)
    
    session.commit()
    session.close()
    print("Seeded database with developers, cloud resources, and developer-resource permissions.")

if __name__ == "__main__":
    seed()
