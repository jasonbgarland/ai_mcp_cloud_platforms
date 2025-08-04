import requests


def register_tools(mcp):
    # Example tool
    @mcp.tool
    def hello(name: str) -> str:
        """Say hello to a user by name."""
        return f"Hello, {name}!"

    @mcp.tool
    def test_simple(test_param: str = "default") -> list:
        """Simple test tool that just returns hardcoded data."""
        return [{"test": "This is a simple test response", "param": test_param}]

    @mcp.tool
    def lookup_resources_for_developer(developer_id: int, cloud_type: str = None) -> dict:
        """Look up resources for a developer."""
        import os
        
        # Get API URL from environment variable
        api_url = os.environ.get("API_URL", "http://localhost:8000")
        
        try:
            # First, verify the developer exists
            dev_response = requests.get(f"{api_url}/developers/{developer_id}")
            if dev_response.status_code == 404:
                return {"error": f"Developer with ID {developer_id} not found"}
            elif dev_response.status_code != 200:
                return {"error": f"Failed to fetch developer: {dev_response.status_code}"}
            
            developer = dev_response.json()
            
            # Use the new enhanced route to get permissions with resource details
            perms_response = requests.get(f"{api_url}/permissions/by-developer/{developer_id}")
            if perms_response.status_code == 404:
                return {"error": f"Developer with ID {developer_id} not found"}
            elif perms_response.status_code != 200:
                return {"error": f"Failed to fetch permissions: {perms_response.status_code}"}
            
            permissions = perms_response.json()
            
            # Filter resources by cloud_type if provided and format the response
            resources = []
            for perm in permissions:
                resource = perm["cloud_resource"]
                
                # Filter by cloud_type if provided
                if cloud_type is None or resource.get('cloud_type', '').lower() == cloud_type.lower():
                    resources.append({
                        "resource_id": resource["id"],
                        "resource_name": resource["name"],
                        "cloud_type": resource["cloud_type"],
                        "permission_level": perm["permission"]
                    })
            
            return {
                "developer": {
                    "id": developer["id"],
                    "name": developer["name"],
                    "email": developer["email"]
                },
                "resources": resources,
                "total_resources": len(resources),
                "filtered_by_cloud_type": cloud_type,
                "summary": f"Developer '{developer['name']}' has access to {len(resources)} resource(s)" + 
                          (f" of type '{cloud_type}'" if cloud_type else "")
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    @mcp.tool
    def list_developers() -> dict:
        """List all developers in the system."""
        import os
        
        api_url = os.environ.get("API_URL", "http://localhost:8000")
        
        try:
            response = requests.get(f"{api_url}/developers/")
            if response.status_code != 200:
                return {"error": f"Failed to fetch developers: {response.status_code}"}
            
            developers = response.json()
            return {
                "developers": developers,
                "total_count": len(developers),
                "summary": f"Found {len(developers)} developer(s) in the system"
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    @mcp.tool
    def list_cloud_resources(cloud_type: str = None) -> dict:
        """List all cloud resources, optionally filtered by cloud type (AWS, AZURE, GCP)."""
        import os
        
        api_url = os.environ.get("API_URL", "http://localhost:8000")
        
        try:
            response = requests.get(f"{api_url}/cloud_resources/")
            if response.status_code != 200:
                return {"error": f"Failed to fetch cloud resources: {response.status_code}"}
            
            all_resources = response.json()
            
            # Filter by cloud_type if provided
            if cloud_type:
                cloud_type_upper = cloud_type.upper()
                filtered_resources = [r for r in all_resources if r.get('cloud_type', '').upper() == cloud_type_upper]
                return {
                    "resources": filtered_resources,
                    "total_count": len(filtered_resources),
                    "filtered_by": cloud_type_upper,
                    "summary": f"Found {len(filtered_resources)} {cloud_type_upper} resource(s)"
                }
            else:
                return {
                    "resources": all_resources,
                    "total_count": len(all_resources),
                    "summary": f"Found {len(all_resources)} total resource(s)"
                }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    @mcp.tool
    def get_resource_permissions(resource_id: int) -> dict:
        """Get all developers who have permissions for a specific cloud resource."""
        import os
        
        api_url = os.environ.get("API_URL", "http://localhost:8000")
        
        try:
            # First, verify the resource exists
            resource_response = requests.get(f"{api_url}/cloud_resources/{resource_id}")
            if resource_response.status_code == 404:
                return {"error": f"Cloud resource with ID {resource_id} not found"}
            elif resource_response.status_code != 200:
                return {"error": f"Failed to fetch cloud resource: {resource_response.status_code}"}
            
            resource = resource_response.json()
            
            # Get permissions for this resource
            perms_response = requests.get(f"{api_url}/permissions/by-resource/{resource_id}")
            if perms_response.status_code == 404:
                return {"error": f"Cloud resource with ID {resource_id} not found"}
            elif perms_response.status_code != 200:
                return {"error": f"Failed to fetch permissions: {perms_response.status_code}"}
            
            permissions = perms_response.json()
            
            # Format the response
            developers_with_permissions = []
            for perm in permissions:
                developer = perm["developer"]
                developers_with_permissions.append({
                    "developer_id": developer["id"],
                    "developer_name": developer["name"],
                    "developer_email": developer["email"],
                    "permission_level": perm["permission"]
                })
            
            return {
                "resource": {
                    "id": resource["id"],
                    "name": resource["name"],
                    "cloud_type": resource["cloud_type"]
                },
                "developers": developers_with_permissions,
                "total_developers": len(developers_with_permissions),
                "summary": f"Resource '{resource['name']}' ({resource['cloud_type']}) has {len(developers_with_permissions)} developer(s) with permissions"
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}