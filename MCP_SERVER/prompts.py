"""
Predefined prompts for the Cloud Resource MCP Server.
These prompts demonstrate common use cases for developers and administrators.
"""


def register_prompts(mcp):
    """Register prompts with the FastMCP server."""
    
    @mcp.prompt("developer_onboarding")
    def developer_onboarding_prompt(developer_name: str) -> str:
        """Check what cloud resources a developer has access to during onboarding.
        
        Args:
            developer_name: The name of the developer (e.g., 'Alice Smith')
        """
        return f"""
I need to check what cloud resources {developer_name} has access to as part of their onboarding process.

Please use the following tools to gather this information:
1. First, use list_developers to find the developer ID for {developer_name}
2. Then use lookup_resources_for_developer with their ID to see all their cloud access
3. Provide a summary of:
   - Total number of resources they can access
   - Breakdown by cloud provider (AWS, AZURE, GCP)
   - Any resources with full (RW) access that might need special attention

This will help ensure they have the right access for their role.
"""

    @mcp.prompt("security_audit_write_access")
    def security_audit_prompt(cloud_type: str = "all") -> str:
        """Find all developers with write or full access to cloud resources for security auditing.
        
        Args:
            cloud_type: Optional cloud provider filter (AWS, AZURE, GCP, or 'all')
        """
        cloud_filter = f" for {cloud_type}" if cloud_type != "all" else ""
        cloud_param = f" with cloud_type='{cloud_type}'" if cloud_type != "all" else ""
        
        return f"""
I need to conduct a security audit to find all developers who have write (WRITE or RW) access to cloud resources{cloud_filter}.

Please help me by:
1. Using list_developers to get all developers in the system
2. For each developer, use lookup_resources_for_developer{cloud_param} to check their permissions
3. Filter and highlight developers who have:
   - WRITE access to any resources
   - RW (read-write) access to any resources
4. Organize the results by cloud provider and permission level
5. Flag any developers with extensive write access that should be reviewed

This audit will help ensure we follow the principle of least privilege.
"""

    @mcp.prompt("resource_access_investigation")
    def resource_investigation_prompt(resource_name: str) -> str:
        """Investigate who has access to a specific cloud resource for debugging or compliance.
        
        Args:
            resource_name: The name of the cloud resource (e.g., 'AWS S3 Bucket')
        """
        return f"""
I need to investigate who has access to "{resource_name}" for debugging/compliance purposes.

Please help by:
1. Using list_cloud_resources to find the resource ID for "{resource_name}"
2. Using get_resource_permissions with that resource ID to see all developers with access
3. Provide a breakdown showing:
   - All developers who can access this resource
   - Their permission levels (READ, WRITE, RW)
   - Their contact information (email addresses)
   - Any developers with write access who could have made changes

This will help track down who might have modified the resource or can help with troubleshooting.
"""

    @mcp.prompt("cloud_footprint_analysis")
    def cloud_footprint_prompt(cloud_type: str) -> str:
        """Analyze developer access patterns across cloud providers for migration planning.
        
        Args:
            cloud_type: The cloud provider to analyze (AWS, AZURE, GCP)
        """
        return f"""
I need to analyze our {cloud_type} footprint to understand developer access patterns for migration planning.

Please analyze by:
1. Using list_cloud_resources with cloud_type="{cloud_type}" to see all {cloud_type} resources
2. Using list_developers to get all developers
3. For each developer, checking their {cloud_type} access using lookup_resources_for_developer
4. Providing analysis including:
   - Total {cloud_type} resources in the system
   - Number of developers with {cloud_type} access
   - Most commonly accessed {cloud_type} resources
   - Developers with the most {cloud_type} permissions
   - Permission distribution (READ vs WRITE vs RW)

This analysis will help with cloud migration and cost optimization planning.
"""

    @mcp.prompt("high_privilege_review")
    def high_privilege_prompt(minimum_resources: int = 5) -> str:
        """Find developers with the most cloud access for security and compliance reviews.
        
        Args:
            minimum_resources: Minimum number of resources a developer must have access to (default: 5)
        """
        return f"""
I need to identify developers with the most cloud access (at least {minimum_resources} resources) for security review.

Please help by:
1. Using list_developers to get all developers
2. For each developer, using lookup_resources_for_developer to count their total access
3. Filtering to show only developers with access to {minimum_resources}+ resources
4. For high-access developers, provide:
   - Total number of resources they can access
   - Breakdown by cloud provider (AWS, AZURE, GCP)
   - Number of resources with write access (WRITE or RW)
   - Their contact information for follow-up

This review will help ensure we maintain appropriate access controls and identify potential over-privileged accounts.
"""
