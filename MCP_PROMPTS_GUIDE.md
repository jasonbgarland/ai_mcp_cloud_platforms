# MCP Server Prompts Usage Guide

This document explains the 5 predefined prompts available in our Cloud Resource MCP Server and how to use them effectively.

## Available Prompts

### 1. 🆕 **Developer Onboarding** (`developer_onboarding`)

**Use Case**: Check what cloud resources a new developer has access to during onboarding.

**Parameters**:

- `developer_name` (required): The name of the developer (e.g., "Alice Smith")

**Example Usage**:

```
Use the developer_onboarding prompt with developer_name="Alice Smith"
```

**What it does**: Helps HR/IT teams verify that new developers have appropriate access during onboarding by providing a comprehensive breakdown of their cloud resource permissions.

---

### 2. 🔐 **Security Audit - Write Access** (`security_audit_write_access`)

**Use Case**: Find all developers with write or full access to cloud resources for security auditing.

**Parameters**:

- `cloud_type` (optional): Filter by cloud provider ("AWS", "AZURE", "GCP", or "all")

**Example Usage**:

```
Use the security_audit_write_access prompt with cloud_type="AWS"
```

**What it does**: Performs security audits to ensure compliance with the principle of least privilege by identifying developers with write access that may need review.

---

### 3. 🔍 **Resource Access Investigation** (`resource_access_investigation`)

**Use Case**: Investigate who has access to a specific cloud resource for debugging or compliance.

**Parameters**:

- `resource_name` (required): The name of the cloud resource (e.g., "AWS S3 Bucket")

**Example Usage**:

```
Use the resource_access_investigation prompt with resource_name="AWS S3 Bucket"
```

**What it does**: Helps with incident response and troubleshooting by identifying all developers who can access a specific resource, including their permission levels and contact information.

---

### 4. ☁️ **Cloud Footprint Analysis** (`cloud_footprint_analysis`)

**Use Case**: Analyze developer access patterns across cloud providers for migration planning.

**Parameters**:

- `cloud_type` (required): The cloud provider to analyze ("AWS", "AZURE", "GCP")

**Example Usage**:

```
Use the cloud_footprint_analysis prompt with cloud_type="AWS"
```

**What it does**: Provides comprehensive analysis for cloud migration and cost optimization by showing resource distribution, access patterns, and permission levels across cloud providers.

---

### 5. ⚠️ **High Privilege Review** (`high_privilege_review`)

**Use Case**: Find developers with the most cloud access for security and compliance reviews.

**Parameters**:

- `minimum_resources` (optional): Minimum number of resources a developer must have access to (default: 5)

**Example Usage**:

```
Use the high_privilege_review prompt with minimum_resources=10
```

**What it does**: Identifies potentially over-privileged accounts for security reviews by finding developers with access to many resources, helping maintain appropriate access controls.

---

## How to Use These Prompts

### In an MCP Client:

1. Connect to the MCP server at `http://localhost:9001/mcp/`
2. Access the prompts section of your MCP client
3. Select the desired prompt from the list
4. Fill in the required parameters
5. Execute the prompt

### Example Scenarios:

#### Scenario 1: New Developer Onboarding

```
Prompt: developer_onboarding
Parameters: developer_name="Bob Jones"
Result: Complete breakdown of Bob's access across AWS, AZURE, and GCP
```

#### Scenario 2: Security Incident Investigation

```
Prompt: resource_access_investigation
Parameters: resource_name="AWS RDS DB"
Result: List of all developers who can access the database with their permission levels
```

#### Scenario 3: Quarterly Security Review

```
Prompt: high_privilege_review
Parameters: minimum_resources=8
Result: Developers with access to 8+ resources flagged for review
```

## Integration with Existing Tools

These prompts work seamlessly with our existing MCP tools:

- `list_developers`
- `list_cloud_resources`
- `lookup_resources_for_developer`
- `get_resource_permissions`
- `hello` (simple test)
- `test_simple` (testing functionality)

Each prompt provides intelligent guidance on which tools to use and how to combine their results for comprehensive analysis.

## Benefits

✅ **Standardized Workflows**: Consistent approach to common cloud access management tasks  
✅ **Compliance Ready**: Built-in security and audit patterns  
✅ **Time Saving**: Pre-defined prompts eliminate the need to construct complex queries  
✅ **Best Practices**: Incorporates security principles like least privilege  
✅ **Scalable**: Works with any number of developers, resources, and cloud providers

## Sample Data Available

Our seeded database includes:

- **5 developers**: Alice Smith, Bob Jones, Carol Lee, David Kim, Eva Brown
- **15 cloud resources**: 5 each from AWS, AZURE, and GCP
- **55 permission assignments**: Various READ, WRITE, and RW permissions

This makes it easy to test and demonstrate all prompt functionality with realistic data.
