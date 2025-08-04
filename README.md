# Cloud Platform MCP Server Demo

A comprehensive demonstration of a **Model Context Protocol (MCP) server** that enables natural language interaction with cloud resource management through intelligent prompts and tools.

## 🎯 Overview

This project showcases how MCP can transform complex cloud infrastructure management into intuitive, conversational workflows. By connecting an LLM client to our MCP server, users can perform sophisticated cloud resource analysis, security audits, and access management using natural language queries.

**Key Innovation**: Instead of writing complex SQL queries or API calls, users can simply ask: _"Help me onboard Alice Smith"_ or _"Audit all write permissions for AWS resources"_ and get comprehensive, structured responses.

## ✨ Features

### 🤖 **MCP Server Capabilities**

- **6 Core Tools** for cloud resource management
- **5 Predefined Prompts** for common IT workflows
- **Natural Language Interface** via Model Context Protocol
- **Real-time Data Access** through FastAPI backend
- **Multi-Cloud Support** (AWS, Azure, GCP)

### 🔧 **Backend Infrastructure**

- **FastAPI REST API** with full CRUD operations
- **PostgreSQL Database** with optimized schema
- **Docker Orchestration** for easy deployment
- **Health Checks** and monitoring
- **Automatic Data Seeding** with realistic test data

### 🛡️ **Security & Compliance**

- **Permission Auditing** across cloud platforms
- **Access Investigation** for specific resources
- **Privilege Reviews** to identify over-privileged accounts
- **Developer Onboarding** with automated access verification

## 🏗️ Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│    LLM Client       │◄──►│    MCP Server       │◄──►│    FastAPI          │
│                     │    │    (Port 9001)      │    │    (Port 8000)      │
│ • Natural Language  │    │ • 6 Tools           │    │ • CRUD Operations   │
│ • Conversational UI │    │ • 5 Smart Prompts   │    │ • Data Validation   │
│ • Auto Tool Select  │    │ • Protocol Handler  │    │ • Business Logic    │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
                                      │                           │
                                      │                           │
                                      ▼                           ▼
                           ┌─────────────────────────────────────────────┐
                           │            PostgreSQL Database              │
                           │                (Port 5432)                  │
                           │ • Developers Table                          │
                           │ • Cloud Resources Table                     │
                           │ • Permissions Table                         │
                           └─────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)

### 1. Clone and Start

```bash
git clone <repository>
cd ai_mcp_cloud_platforms

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### 2. Verify Installation

```bash
# Test API
curl http://localhost:8000/developers/

# Test MCP Server
curl http://localhost:9001/mcp/

# Run demonstration
python demo_prompts.py
```

### 3. Access Services

- **API Documentation**: http://localhost:8000/docs
- **MCP Server**: http://localhost:9001/mcp/
- **Database**: localhost:5432 (itadmin/itadmin)

## 🔨 Project Structure

```
ai_mcp_cloud_platforms/
├── API/                           # FastAPI Backend
│   ├── main.py                   # API entry point
│   ├── models.py                 # SQLAlchemy models
│   ├── database/
│   │   ├── init_db.sql          # Database schema
│   │   └── connection.py        # DB connection
│   ├── routes/                   # API endpoints
│   │   ├── developers.py        # Developer CRUD
│   │   ├── cloud_resources.py   # Resource CRUD
│   │   └── permissions.py       # Permission CRUD
│   └── Dockerfile               # API container
│
├── MCP_SERVER/                   # MCP Server
│   ├── main.py                  # MCP entry point
│   ├── tools.py                 # 6 MCP tools
│   ├── prompts.py               # 5 predefined prompts
│   └── Dockerfile               # MCP container
│
├── seed_data/                    # Database seeding
│   └── seed_api.py              # Test data generation
│
├── docker-compose.yml            # Service orchestration
├── demo_prompts.py              # Demonstration script
├── MCP_PROMPTS_GUIDE.md         # Prompt documentation
├── PROJECT_SUMMARY.md           # Technical deep dive
└── README.md                    # This file
```

## 🛠️ MCP Server Details

### Tools Available

| Tool                             | Purpose                    | Example Use             |
| -------------------------------- | -------------------------- | ----------------------- |
| `list_developers`                | Get all developers         | User management         |
| `list_cloud_resources`           | Get resources (filterable) | Resource inventory      |
| `lookup_resources_for_developer` | User's access              | Onboarding verification |
| `get_resource_permissions`       | Resource access list       | Security investigation  |
| `hello`                          | Simple greeting            | Connectivity test       |
| `test_simple`                    | Basic functionality        | Health check            |

### Intelligent Prompts

| Prompt                          | Scenario           | Business Value                  |
| ------------------------------- | ------------------ | ------------------------------- |
| `developer_onboarding`          | New hire setup     | Streamlined access verification |
| `security_audit_write_access`   | Compliance review  | Risk assessment                 |
| `resource_access_investigation` | Incident response  | Quick access lookup             |
| `cloud_footprint_analysis`      | Migration planning | Cost optimization               |
| `high_privilege_review`         | Security audit     | Privilege management            |

## 🎮 How to Interact

### Via API (Direct)

```bash
# Get all developers
curl http://localhost:8000/developers/

# Get permissions for developer ID 1
curl http://localhost:8000/permissions/by-developer/1

# Get who can access resource ID 1
curl http://localhost:8000/permissions/by-resource/1
```

### Via MCP (Natural Language)

With an MCP-compatible LLM client:

```
User: "Help me onboard developer Alice Smith"
LLM: Uses developer_onboarding prompt → Shows Alice's resources across clouds

User: "Who has write access to AWS resources?"
LLM: Uses security_audit_write_access prompt → Lists write permissions

User: "Investigate access to the AWS S3 Bucket"
LLM: Uses resource_access_investigation prompt → Shows detailed access
```

### Via Demo Script

```bash
python demo_prompts.py
```

This runs all 5 prompts with real data and shows exactly what an LLM would see.

## 📊 Sample Data

The system comes pre-loaded with realistic test data:

### Developers (5)

- Alice Smith, Bob Jones, Carol Lee, David Kim, Eva Brown

### Cloud Resources (15)

- **AWS**: S3 Bucket, EC2 Instance, RDS DB, Lambda Function, DynamoDB Table
- **Azure**: VM, Blob Storage, SQL Database, App Service, Cosmos DB
- **GCP**: BigQuery, Compute Engine, Cloud Storage, Cloud SQL, Pub/Sub

### Permissions (55)

- Realistic distribution of READ, WRITE, and RW permissions
- Multi-cloud access patterns
- Varying privilege levels per developer

## 🔧 Development

### Local Development Setup

```bash
# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary
pip install fastmcp

# Start PostgreSQL (via Docker)
docker-compose up demo-db -d

# Run API locally
cd API && python -m uvicorn main:app --reload --port 8000

# Run MCP Server locally
cd MCP_SERVER && python main.py
```

### Adding New Tools

1. Define tool function in `MCP_SERVER/tools.py`
2. Add `@mcp.tool()` decorator
3. Register in `main.py`
4. Test with demo script

### Adding New Prompts

1. Create prompt function in `MCP_SERVER/prompts.py`
2. Add `@mcp.prompt()` decorator
3. Register in `main.py`
4. Document in `MCP_PROMPTS_GUIDE.md`

## 🐳 Docker Services

| Service           | Purpose               | Port | Health Check |
| ----------------- | --------------------- | ---- | ------------ |
| `demo-db`         | PostgreSQL database   | 5432 | `pg_isready` |
| `demo-db-setup`   | Schema initialization | -    | One-time     |
| `demo-db-seed`    | Test data loading     | -    | One-time     |
| `demo-api`        | FastAPI backend       | 8000 | HTTP `/`     |
| `demo-mcp-server` | MCP server            | 9001 | HTTP `/mcp/` |

### Environment Variables

```env
POSTGRES_USER=itadmin
POSTGRES_PASSWORD=itadmin
POSTGRES_DB=demo_db
POSTGRES_HOST=demo-db
POSTGRES_PORT=5432
API_BASE_URL=http://demo-api:8000
```

## 🧪 Testing

### API Testing

```bash
# Health check
curl http://localhost:8000/

# Get all developers
curl http://localhost:8000/developers/ | jq

# Test filtering
curl http://localhost:8000/cloud_resources/?cloud_type=AWS | jq
```

### MCP Testing

```bash
# Run full demonstration
python demo_prompts.py

# Test specific scenarios
python -c "
import requests
print(requests.get('http://localhost:8000/permissions/by-developer/1').json())
"
```

## 🎯 Use Cases

### 1. **IT Operations**

- Automate developer onboarding workflows
- Generate access reports for compliance
- Investigate security incidents quickly
- Plan cloud migrations with access analysis

### 2. **Security Teams**

- Audit permissions across cloud platforms
- Identify over-privileged accounts
- Track resource access patterns
- Generate compliance reports

### 3. **DevOps Teams**

- Verify developer access during deployments
- Analyze cloud resource utilization
- Manage multi-cloud permissions centrally
- Streamline access reviews

## 🚀 Extending the Project

### Potential Enhancements

- **Cost Tracking**: Add cloud cost data to resources
- **Time-based Access**: Implement temporary permissions
- **Approval Workflows**: Add permission request/approval
- **Alert System**: Notify on unusual access patterns
- **Multi-tenant**: Support multiple organizations
- **Resource Tagging**: Add metadata and categorization

### Integration Ideas

- **LDAP/Active Directory**: Sync with corporate identity
- **Cloud Provider APIs**: Real-time resource discovery
- **Slack/Teams**: Chat-based access requests
- **Monitoring Tools**: Integration with DataDog, New Relic
- **CI/CD Pipelines**: Automated access verification

## 📚 Documentation

- **API Documentation**: Auto-generated at http://localhost:8000/docs
- **MCP Prompts Guide**: See [MCP_PROMPTS_GUIDE.md](MCP_PROMPTS_GUIDE.md)
- **Technical Deep Dive**: See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Database Schema**: See `API/database/init_db.sql`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📄 License

This project is provided as a demonstration of MCP capabilities. See LICENSE file for details.

## 🙋‍♂️ Support

For questions about this MCP server demonstration:

- Review the [MCP_PROMPTS_GUIDE.md](MCP_PROMPTS_GUIDE.md) for prompt usage
- Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for technical details
- Run `python demo_prompts.py` to see the system in action

---

**🎉 Ready to see AI-powered cloud management in action?**

Run `docker-compose up -d` and then `python demo_prompts.py` to experience how natural language can transform complex cloud infrastructure tasks into simple conversations!
