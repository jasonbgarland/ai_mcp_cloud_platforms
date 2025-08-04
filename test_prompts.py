#!/usr/bin/env python3
"""
Test script to demonstrate the MCP Server prompts in action.
This script simulates how an LLM would interact with our MCP server prompts.
"""

import requests
from typing import Dict, Any

# MCP Server endpoint
MCP_BASE_URL = "http://localhost:9001/mcp"

def call_mcp_tool(tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Call an MCP tool directly via HTTP."""
    url = f"{MCP_BASE_URL}/tools/call"
    payload = {
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": parameters
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def test_developer_onboarding():
    """Test the developer onboarding prompt scenario."""
    print("\n🔹 Testing Developer Onboarding Prompt")
    print("=" * 50)
    
    # This would typically be called by an LLM using the prompt
    # For demonstration, we'll call the underlying tool directly
    result = call_mcp_tool("lookup_resources_for_developer", {"developer_id": 1})
    
    print("Developer Alice Smith's resources:")
    if "result" in result:
        resources = result["result"]
        print(f"Found {len(resources)} resources:")
        for resource in resources[:3]:  # Show first 3
            print(f"  - {resource['resource_name']} ({resource['cloud_type']}) - {resource['permission_type']} access")
        if len(resources) > 3:
            print(f"  ... and {len(resources) - 3} more resources")
    else:
        print(f"Error: {result}")

def test_security_audit():
    """Test the security audit prompt scenario."""
    print("\n🔹 Testing Security Audit (Write Access) Prompt")
    print("=" * 50)
    
    # Get all AWS resources with write permissions
    result = call_mcp_tool("list_cloud_resources", {"cloud_type": "AWS"})
    
    if "result" in result:
        aws_resources = result["result"]
        print(f"Found {len(aws_resources)} AWS resources")
        
        # For each resource, check who has write access
        write_access_count = 0
        for resource in aws_resources[:3]:  # Check first 3
            perms_result = call_mcp_tool("get_resource_permissions", {"resource_id": resource["id"]})
            if "result" in perms_result:
                write_perms = [p for p in perms_result["result"] if p["permission_type"] in ["WRITE", "RW"]]
                if write_perms:
                    write_access_count += len(write_perms)
                    print(f"  {resource['name']}: {len(write_perms)} users with write access")
        
        print(f"\nTotal write permissions found: {write_access_count}")
    else:
        print(f"Error: {result}")

def test_resource_investigation():
    """Test the resource access investigation prompt scenario."""
    print("\n🔹 Testing Resource Access Investigation Prompt")
    print("=" * 50)
    
    # Investigate who has access to AWS S3 Bucket (resource ID 1)
    result = call_mcp_tool("get_resource_permissions", {"resource_id": 1})
    
    if "result" in result:
        permissions = result["result"]
        print("AWS S3 Bucket access permissions:")
        print(f"Found {len(permissions)} users with access:")
        
        for perm in permissions:
            print(f"  - {perm['developer_name']}: {perm['permission_type']} access")
    else:
        print(f"Error: {result}")

def test_cloud_footprint():
    """Test the cloud footprint analysis prompt scenario."""
    print("\n🔹 Testing Cloud Footprint Analysis Prompt")
    print("=" * 50)
    
    # Analyze GCP footprint
    result = call_mcp_tool("list_cloud_resources", {"cloud_type": "GCP"})
    
    if "result" in result:
        gcp_resources = result["result"]
        print("GCP Cloud Footprint Analysis:")
        print(f"Total GCP resources: {len(gcp_resources)}")
        
        # Count by resource type
        resource_types = {}
        for resource in gcp_resources:
            res_type = resource["name"].split()[1] if len(resource["name"].split()) > 1 else "Unknown"
            resource_types[res_type] = resource_types.get(res_type, 0) + 1
        
        print("Resource breakdown:")
        for res_type, count in resource_types.items():
            print(f"  - {res_type}: {count}")
    else:
        print(f"Error: {result}")

def test_high_privilege_review():
    """Test the high privilege review prompt scenario."""
    print("\n🔹 Testing High Privilege Review Prompt")
    print("=" * 50)
    
    # Find developers with many resource assignments
    all_developers = call_mcp_tool("list_developers", {})
    
    if "result" in all_developers:
        developers = all_developers["result"]
        high_privilege_devs = []
        
        for dev in developers:
            resources_result = call_mcp_tool("lookup_resources_for_developer", {"developer_id": dev["id"]})
            if "result" in resources_result:
                resource_count = len(resources_result["result"])
                if resource_count >= 8:  # High privilege threshold
                    high_privilege_devs.append((dev["name"], resource_count))
        
        print("High-privilege developers (8+ resources):")
        for name, count in high_privilege_devs:
            print(f"  - {name}: {count} resources")
        
        print(f"\nTotal high-privilege users: {len(high_privilege_devs)}")
    else:
        print(f"Error: {all_developers}")

def main():
    """Run all prompt tests."""
    print("🚀 MCP Server Prompt Demonstration")
    print("=" * 50)
    print("This script demonstrates the 5 predefined prompts in action.")
    print("In a real scenario, these would be triggered by LLM conversations.")
    
    try:
        test_developer_onboarding()
        test_security_audit()
        test_resource_investigation()
        test_cloud_footprint()
        test_high_privilege_review()
        
        print("\n" + "=" * 50)
        print("✅ All prompt demonstrations completed successfully!")
        print("\n💡 To use these prompts with an LLM:")
        print("1. Connect your LLM to the MCP server at http://localhost:9001/mcp/")
        print("2. Use prompts like: 'Help me onboard developer Alice Smith'")
        print("3. The LLM will automatically use the appropriate MCP tools")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Test failed with network error: {str(e)}")
    except ValueError as e:
        print(f"\n❌ Test failed with data error: {str(e)}")

if __name__ == "__main__":
    main()
