#!/usr/bin/env python3
"""
Direct API test to demonstrate the data that our MCP prompts would work with.
This shows the actual functionality behind our 5 MCP prompts.
"""

import requests
from typing import Dict, Any

# API endpoint
API_BASE_URL = "http://localhost:8000"

def call_api(endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
    """Call the API directly."""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        response.raise_for_status()
        return {"result": response.json()}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def demonstrate_developer_onboarding():
    """Demonstrate what the developer_onboarding prompt would show."""
    print("\n🎯 PROMPT 1: Developer Onboarding")
    print("=" * 50)
    print("Scenario: 'Help me onboard developer Alice Smith'")
    print("The MCP server would run these API calls:")
    
    # Get developer info
    developers = call_api("/developers/")
    if "result" in developers:
        alice = next((d for d in developers["result"] if d["name"] == "Alice Smith"), None)
        if alice:
            print(f"\n✅ Found developer: {alice['name']} (ID: {alice['id']})")
            
            # Get their resources
            resources = call_api(f"/permissions/by-developer/{alice['id']}")
            if "result" in resources:
                print(f"📋 Alice has access to {len(resources['result'])} resources:")
                
                # Group by cloud type
                cloud_summary = {}
                for resource in resources["result"]:
                    cloud = resource["cloud_resource"]["cloud_type"]
                    if cloud not in cloud_summary:
                        cloud_summary[cloud] = {"total": 0, "write": 0}
                    cloud_summary[cloud]["total"] += 1
                    if resource["permission"] in ["WRITE", "RW"]:
                        cloud_summary[cloud]["write"] += 1
                
                for cloud, stats in cloud_summary.items():
                    print(f"  {cloud}: {stats['total']} resources ({stats['write']} with write access)")
                
                print("\n📝 Onboarding checklist for Alice:")
                print("  ✓ Verify account access credentials")
                print("  ✓ Review security policies for write permissions")  
                print("  ✓ Schedule training session for cloud resources")
                print("  ✓ Confirm backup access procedures")

def demonstrate_security_audit():
    """Demonstrate what the security_audit_write_access prompt would show."""
    print("\n🎯 PROMPT 2: Security Audit (Write Access)")
    print("=" * 50)
    print("Scenario: 'Audit all write permissions for AWS resources'")
    print("The MCP server would run these API calls:")
    
    # Get all AWS resources
    resources = call_api("/cloud_resources/")
    if "result" in resources:
        aws_resources = [r for r in resources["result"] if r["cloud_type"] == "AWS"]
        print(f"\n✅ Found {len(aws_resources)} AWS resources")
        
        total_write_permissions = 0
        high_risk_resources = []
        
        for resource in aws_resources:
            permissions = call_api(f"/permissions/by-resource/{resource['id']}")
            if "result" in permissions:
                write_perms = [p for p in permissions["result"] 
                             if p["permission"] in ["WRITE", "RW"]]
                total_write_permissions += len(write_perms)
                
                if len(write_perms) >= 2:  # High risk threshold
                    high_risk_resources.append((resource["name"], len(write_perms)))
        
        print("🔍 Security audit results:")
        print(f"  Total write permissions: {total_write_permissions}")
        print(f"  High-risk resources (2+ write users): {len(high_risk_resources)}")
        
        if high_risk_resources:
            print("  ⚠️  Resources requiring review:")
            for name, count in high_risk_resources[:3]:
                print(f"     - {name}: {count} users with write access")

def demonstrate_resource_investigation():
    """Demonstrate what the resource_access_investigation prompt would show."""
    print("\n🎯 PROMPT 3: Resource Access Investigation")
    print("=" * 50)
    print("Scenario: 'Who has access to the AWS S3 Bucket?'")
    print("The MCP server would run these API calls:")
    
    # Find AWS S3 Bucket
    resources = call_api("/cloud_resources/")
    if "result" in resources:
        s3_bucket = next((r for r in resources["result"] 
                         if "S3 Bucket" in r["name"]), None)
        if s3_bucket:
            print(f"\n✅ Found resource: {s3_bucket['name']} (ID: {s3_bucket['id']})")
            
            # Get permissions
            permissions = call_api(f"/permissions/by-resource/{s3_bucket['id']}")
            if "result" in permissions:
                print("🔍 Access investigation results:")
                print(f"  Total users with access: {len(permissions['result'])}")
                
                # Categorize by permission type
                perm_types = {}
                for perm in permissions["result"]:
                    ptype = perm["permission"]
                    perm_types[ptype] = perm_types.get(ptype, 0) + 1
                
                print("  Permission breakdown:")
                for ptype, count in perm_types.items():
                    print(f"    {ptype}: {count} users")
                
                print("\n  👥 User access details:")
                for perm in permissions["result"]:
                    print(f"    - {perm['developer']['name']}: {perm['permission']} access")

def demonstrate_cloud_footprint():
    """Demonstrate what the cloud_footprint_analysis prompt would show."""
    print("\n🎯 PROMPT 4: Cloud Footprint Analysis")
    print("=" * 50)
    print("Scenario: 'Analyze our GCP cloud footprint'")
    print("The MCP server would run these API calls:")
    
    # Get all GCP resources
    resources = call_api("/cloud_resources/")
    if "result" in resources:
        gcp_resources = [r for r in resources["result"] if r["cloud_type"] == "GCP"]
        print(f"\n✅ Found {len(gcp_resources)} GCP resources")
        
        # Analyze resource types
        resource_types = {}
        total_permissions = 0
        
        for resource in gcp_resources:
            # Extract resource type from name
            parts = resource["name"].split()
            if len(parts) >= 2:
                resource_type = parts[1]
            else:
                resource_type = "Unknown"
            
            resource_types[resource_type] = resource_types.get(resource_type, 0) + 1
            
            # Count permissions
            permissions = call_api(f"/permissions/by-resource/{resource['id']}")
            if "result" in permissions:
                total_permissions += len(permissions["result"])
        
        print("📊 GCP footprint analysis:")
        print(f"  Total resources: {len(gcp_resources)}")
        print(f"  Total user permissions: {total_permissions}")
        print("  Resource distribution:")
        
        for res_type, count in sorted(resource_types.items()):
            print(f"    {res_type}: {count}")
        
        avg_perms = total_permissions / len(gcp_resources) if gcp_resources else 0
        print(f"  Average permissions per resource: {avg_perms:.1f}")

def demonstrate_high_privilege_review():
    """Demonstrate what the high_privilege_review prompt would show."""
    print("\n🎯 PROMPT 5: High Privilege Review")
    print("=" * 50)
    print("Scenario: 'Show me users with access to 8+ resources'")
    print("The MCP server would run these API calls:")
    
    # Get all developers
    developers = call_api("/developers/")
    if "result" in developers:
        print(f"\n✅ Found {len(developers['result'])} developers")
        
        high_privilege_users = []
        all_user_stats = []
        
        for dev in developers["result"]:
            # Get their resources
            resources = call_api(f"/permissions/by-developer/{dev['id']}")
            if "result" in resources:
                resource_count = len(resources["result"])
                write_count = len([r for r in resources["result"] 
                                 if r["permission"] in ["WRITE", "RW"]])
                
                all_user_stats.append({
                    "name": dev["name"],
                    "total_resources": resource_count,
                    "write_resources": write_count
                })
                
                if resource_count >= 8:  # High privilege threshold
                    high_privilege_users.append({
                        "name": dev["name"],
                        "total_resources": resource_count,
                        "write_resources": write_count
                    })
        
        print("🔍 Privilege analysis results:")
        print(f"  Users with 8+ resources: {len(high_privilege_users)}")
        
        if high_privilege_users:
            print("  ⚠️  High-privilege users requiring review:")
            for user in high_privilege_users:
                print(f"     - {user['name']}: {user['total_resources']} total "
                      f"({user['write_resources']} write permissions)")
        else:
            print("  ✅ No users with excessive privileges found")
        
        # Show distribution
        avg_resources = sum(u["total_resources"] for u in all_user_stats) / len(all_user_stats)
        print(f"  Average resources per user: {avg_resources:.1f}")
        
        # Show all users for context
        print("\n  📊 All user resource counts:")
        for user in sorted(all_user_stats, key=lambda x: x["total_resources"], reverse=True):
            print(f"     - {user['name']}: {user['total_resources']} resources "
                  f"({user['write_resources']} write)")

def main():
    """Run all prompt demonstrations."""
    print("🚀 MCP Server Prompt Functionality Demonstration")
    print("=" * 60)
    print("This shows what each of our 5 MCP prompts would accomplish")
    print("when used by an LLM client.")
    
    try:
        demonstrate_developer_onboarding()
        demonstrate_security_audit()
        demonstrate_resource_investigation()
        demonstrate_cloud_footprint()
        demonstrate_high_privilege_review()
        
        print("\n" + "=" * 60)
        print("✅ All prompt demonstrations completed!")
        print("\n💡 In a real MCP setup:")
        print("1. An LLM connects to our MCP server")
        print("2. User asks: 'Help me onboard Alice Smith'")
        print("3. LLM uses our developer_onboarding prompt")
        print("4. MCP tools automatically fetch the data shown above")
        print("5. LLM formats a helpful response for the user")
        
        print("\n🔗 MCP Server running at: http://localhost:9001/mcp/")
        print("📚 See MCP_PROMPTS_GUIDE.md for integration details")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Demonstration interrupted by user")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Failed to connect to API: {str(e)}")
        print("Make sure the API is running on http://localhost:8000")

if __name__ == "__main__":
    main()
