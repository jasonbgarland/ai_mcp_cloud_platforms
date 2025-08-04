from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["root"])
def read_root():
    return {"message": "API server is running."}

# Import and include developer router

from routes.cloud_resource.routes import router as cloud_resource_router
from routes.developer.routes import router as developer_router
from routes.permission.routes import router as permission_router

app.include_router(developer_router)
app.include_router(cloud_resource_router)
app.include_router(permission_router)
