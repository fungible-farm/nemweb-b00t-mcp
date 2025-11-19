# _b00t_ Integration Guide for nemweb-b00t-mcp

## Overview

This guide explains how nemweb-b00t-mcp integrates with the elasticdotventures/_b00t_ framework to provide agentic capabilities for AEMO energy data access and processing.

## What is _b00t_?

_b00t_ (pronounced "boot") is an **agentic hive operating system** that provides:

- 🧠 **Context Management**: AI agents gain full environmental awareness
- 🔧 **Universal Tooling**: Seamless access to 100+ development tools  
- 🐝 **Hive Coordination**: Multi-agent collaboration via ACP (Agent Coordination Protocol)
- 📚 **Tribal Knowledge**: LFMF (Learn From My Failures) system captures lessons learned
- 🎯 **Mission Control**: Structured task management with dependency resolution
- 🔒 **Security**: JWT-based namespace isolation and permission enforcement

## _b00t_ Framework Architecture

### Core Components

#### 1. MCP (Model Context Protocol) Integration

MCP is the standard protocol for connecting AI agents to external tools. _b00t_ provides:

- **MCP Servers**: Expose functionality as discoverable tools
- **Tool Registry**: Catalog of available capabilities
- **ACL System**: Permission-based access control
- **Session Management**: Authenticated agent sessions

#### 2. ACP (Agent Coordination Protocol)

Enables multi-agent workflows through:

- **Message Types**: STATUS, PROPOSE, STEP
- **Step Barriers**: Synchronization points for coordinated actions
- **Hive Missions**: Multi-agent task orchestration
- **Voting**: Consensus-based decision making

#### 3. Skill System

Organized knowledge for agents via `b00t learn`:

- **Skill Templates**: Markdown documents with tool usage patterns
- **Contextual Loading**: Load skills only when needed
- **Tribal Knowledge**: Accumulated wisdom from agent experiences
- **LFMF Database**: Documented failure patterns and solutions

#### 4. Task Automation (justfile)

Using casey/just for:

- Repeatable commands
- Complex workflows
- Development automation
- Deployment procedures

## nemweb Integration with _b00t_

### Current nemweb Capabilities

The original nemweb package provides:

1. **Data Download**: Fetch AEMO data files from nemweb.com.au
2. **File Processing**: Parse CSV files from zip archives
3. **Database Storage**: Insert data into SQLite tables
4. **Dataset Management**: Handle multiple dataset types
5. **Incremental Updates**: Download only new data

### _b00t_-Enhanced Capabilities

After integration, agents will be able to:

1. **Discover**: Find available AEMO datasets via MCP
2. **Download**: Fetch data with simple tool calls
3. **Query**: Run SQL queries against stored data
4. **Monitor**: Check data freshness and status
5. **Coordinate**: Multi-agent data pipeline orchestration
6. **Learn**: Access AEMO domain knowledge via skills

## Agent Experience

### Before _b00t_ Integration

```python
# Agent needs to know Python API, file locations, configuration
from nemweb import nemweb_current

# Must manually configure database location
nemweb_current.update_datasets(['dispatch_scada'])
# Prompted for start date if table doesn't exist

# Must know SQL to query results
import sqlite3
conn = sqlite3.connect('/path/to/db.db')
cur = conn.cursor()
results = cur.execute("SELECT * FROM DISPATCH_UNIT_SCADA").fetchall()
```

**Problems:**
- Agent must understand Python APIs
- File paths and configuration are unclear
- No discovery mechanism
- No coordination between agents
- Errors are cryptic

### After _b00t_ Integration

```bash
# Agent discovers available tools
b00t mcp list nemweb

# Agent learns about nemweb capabilities
b00t learn nemweb

# Agent downloads data with one command
b00t mcp call nemweb nemweb_download \
  --dataset dispatch_scada \
  --start-date 20240101 \
  --end-date 20240131

# Agent queries data
b00t mcp call nemweb nemweb_query \
  --sql "SELECT AVG(SCADAVALUE) FROM DISPATCH_UNIT_SCADA WHERE DUID='AGLHAL'"

# Multi-agent coordination
b00t acp hive create data-pipeline 3 "Download Q1 2024 data"
# Workers automatically distribute dataset downloads
```

**Benefits:**
- ✅ Self-documenting tools
- ✅ Automatic configuration
- ✅ Clear error messages with LFMF guidance
- ✅ Multi-agent coordination built-in
- ✅ Progress reporting and monitoring

## MCP Tools Specification

### Tool: nemweb_discover

**Description**: List all available AEMO datasets

**Parameters**: None

**Returns**: 
```json
{
  "datasets": [
    {
      "name": "dispatch_scada",
      "description": "Dispatch SCADA data",
      "update_frequency": "5min",
      "tables": ["DISPATCH_UNIT_SCADA"]
    },
    {
      "name": "trading_is",
      "description": "Trading Interval Summary",
      "update_frequency": "30min", 
      "tables": ["TRADING_PRICE", "TRADING_REGIONSUM"]
    }
  ]
}
```

### Tool: nemweb_download

**Description**: Download dataset for specified date range

**Parameters**:
- `dataset` (string, required): Dataset name
- `start_date` (string, required): Start date (YYYYMMDD)
- `end_date` (string, optional): End date (YYYYMMDD), defaults to today
- `db_name` (string, optional): Database name, defaults to 'nemweb.db'

**Returns**:
```json
{
  "status": "success",
  "records_inserted": 12450,
  "time_range": "2024-01-01 to 2024-01-31",
  "database": "/home/user/.b00t/data/nemweb.db"
}
```

### Tool: nemweb_query

**Description**: Execute SQL query against nemweb database

**Parameters**:
- `sql` (string, required): SQL query to execute
- `db_name` (string, optional): Database name
- `limit` (integer, optional): Maximum rows to return

**Returns**:
```json
{
  "columns": ["DUID", "SCADAVALUE", "SETTLEMENTDATE"],
  "rows": [
    ["AGLHAL", 150.5, "2024-01-01 00:05:00"],
    ["AGLSOM", 200.0, "2024-01-01 00:05:00"]
  ],
  "row_count": 2
}
```

### Tool: nemweb_update

**Description**: Update datasets to current date

**Parameters**:
- `datasets` (array, optional): List of datasets to update, or --all
- `db_name` (string, optional): Database name

**Returns**:
```json
{
  "updated": ["dispatch_scada", "trading_is"],
  "records_added": 5420,
  "last_update": "2024-11-19T07:52:32Z"
}
```

### Tool: nemweb_status

**Description**: Check data freshness and status

**Parameters**:
- `db_name` (string, optional): Database name

**Returns**:
```json
{
  "datasets": [
    {
      "name": "dispatch_scada",
      "latest_date": "2024-11-19",
      "record_count": 1245000,
      "size_mb": 450.5,
      "freshness": "current"
    }
  ],
  "database_size_mb": 1250.0,
  "database_path": "/home/user/.b00t/data/nemweb.db"
}
```

### Tool: nemweb_schema

**Description**: Get table schema information

**Parameters**:
- `table` (string, optional): Specific table name
- `db_name` (string, optional): Database name

**Returns**:
```json
{
  "tables": [
    {
      "name": "DISPATCH_UNIT_SCADA",
      "columns": [
        {"name": "SETTLEMENTDATE", "type": "TEXT"},
        {"name": "DUID", "type": "TEXT"},
        {"name": "SCADAVALUE", "type": "REAL"}
      ],
      "row_count": 1245000
    }
  ]
}
```

## Skill Definitions

### Skill: nemweb (Master Skill)

Located: `skills/nemweb/README-nemweb.md`

**Contents**:
- Overview of AEMO and nemweb
- Available datasets
- Common workflows
- Tool usage examples
- Troubleshooting guide
- LFMF knowledge base

**Usage**:
```bash
b00t learn nemweb
```

### Skill: aemo-data

Located: `skills/nemweb/aemo-data.md`

**Contents**:
- AEMO data structure
- Dataset schemas
- Update frequencies
- Data quality considerations
- Historical data availability

### Skill: dispatch

Located: `skills/nemweb/dispatch.md`

**Contents**:
- Dispatch process overview
- SCADA data interpretation
- 5-minute dispatch intervals
- Generation unit identifiers (DUID)
- Dispatch prices and quantities

### Skill: trading

Located: `skills/nemweb/trading.md`

**Contents**:
- Trading interval (30-min) structure
- Regional pricing
- Demand forecasting
- Price setting mechanisms

## Multi-Agent Coordination Patterns

### Pattern 1: Parallel Dataset Download

**Scenario**: Download multiple datasets for the same time period

```bash
# Captain agent creates mission
b00t acp hive create data-download 3 "Download Q1 2024 data" captain

# Worker 1 joins and takes dispatch_scada
b00t acp hive join data-download worker1
b00t mcp call nemweb nemweb_download --dataset dispatch_scada --start-date 20240101 --end-date 20240331
b00t acp hive ready data-download 1

# Worker 2 joins and takes trading_is
b00t acp hive join data-download worker2
b00t mcp call nemweb nemweb_download --dataset trading_is --start-date 20240101 --end-date 20240331
b00t acp hive ready data-download 1

# Worker 3 joins and takes rooftopPV_actual
b00t acp hive join data-download worker3
b00t mcp call nemweb nemweb_download --dataset rooftopPV_actual --start-date 20240101 --end-date 20240331
b00t acp hive ready data-download 1

# Captain waits for all workers
b00t acp hive sync data-download 1

# Step 2: Verify data quality
# All workers check their datasets
b00t acp hive sync data-download 2

# Mission complete
```

### Pattern 2: Data Quality Validation

**Scenario**: Multiple agents validate downloaded data

```bash
# Captain creates validation mission
b00t acp hive create validation 2 "Validate Q1 data" captain

# Worker 1: Check for missing dates
b00t mcp call nemweb nemweb_query --sql "SELECT COUNT(DISTINCT DATE(SETTLEMENTDATE)) FROM DISPATCH_UNIT_SCADA WHERE SETTLEMENTDATE >= '2024-01-01' AND SETTLEMENTDATE < '2024-04-01'"
# Expected: 91 days

# Worker 2: Check for data anomalies
b00t mcp call nemweb nemweb_query --sql "SELECT COUNT(*) FROM DISPATCH_UNIT_SCADA WHERE SCADAVALUE < 0 OR SCADAVALUE > 10000"
# Should be minimal

# Vote on data quality
b00t acp vote create validation "Data quality acceptable?"
# Workers vote based on their checks
```

### Pattern 3: Incremental Update Pipeline

**Scenario**: Continuously update data as new files become available

```bash
# Captain monitors for new data
while true; do
  # Check if new data available
  current_latest=$(b00t mcp call nemweb nemweb_status | jq -r '.datasets[0].latest_date')
  
  # If data is old, trigger update
  if [[ "$current_latest" < "$(date +%Y-%m-%d)" ]]; then
    b00t acp hive create update 1 "Daily data update" captain
    b00t mcp call nemweb nemweb_update --all
    b00t acp hive ready update 1
  fi
  
  sleep 3600  # Check hourly
done
```

## LFMF (Learn From My Failures) Examples

### Failure: SQLite Database Locked

**Context**: Multiple agents trying to write to SQLite simultaneously

**Symptom**: `sqlite3.OperationalError: database is locked`

**Solution**: 
```bash
# Enable WAL mode for concurrent access
b00t lfmf nemweb "SQLite locked: Enable WAL mode with 'PRAGMA journal_mode=WAL' before concurrent writes"
```

**Prevention**:
- Use WAL (Write-Ahead Logging) mode
- Implement connection pooling
- Retry logic with exponential backoff

### Failure: Missing Start Date

**Context**: First-time download of dataset prompts for start date

**Symptom**: Interactive prompt blocks agent execution

**Solution**:
```bash
b00t lfmf nemweb "Missing start date: Always provide --start-date parameter, never rely on interactive prompts in agent workflows"
```

**Prevention**:
- Always specify start_date in tool calls
- MCP tools don't support interactive prompts
- Use default start date if not specified

### Failure: Network Timeout

**Context**: Large dataset download fails due to network timeout

**Symptom**: `requests.exceptions.ReadTimeout`

**Solution**:
```bash
b00t lfmf nemweb "Network timeout: Split large date ranges into smaller chunks (e.g., weekly instead of yearly) and use retry logic"
```

**Prevention**:
- Download in smaller date ranges
- Implement automatic retry with backoff
- Add progress reporting for long downloads

## Configuration Examples

### b00t-mcp.json (Full Example)

```json
{
  "mcpServers": {
    "nemweb": {
      "command": "python",
      "args": ["-m", "b00t_mcp_nemweb.server"],
      "env": {
        "NEMWEB_DB_DIR": "${HOME}/.b00t/data",
        "NEMWEB_CACHE_DIR": "${HOME}/.b00t/cache/nemweb",
        "NEMWEB_LOG_LEVEL": "INFO"
      },
      "capabilities": {
        "tools": true,
        "resources": false,
        "prompts": false
      }
    }
  }
}
```

### b00t-mcp-acl.toml (Full Example)

```toml
# nemweb Access Control List

[permissions]
# Read access to data
read_data = [
    "account.engineering.data-analyst",
    "account.engineering.ai-assistant",
    "account.analytics.*"
]

# Write access (download new data)
write_data = [
    "account.engineering.data-engineer",
    "account.engineering.etl-worker"
]

# Admin access (schema changes, database management)
admin = [
    "account.engineering.admin",
    "account.engineering.dba"
]

[rate_limits]
# Per-agent limits
download_per_hour = 100
query_per_minute = 60
update_per_day = 24

[datasets]
# Dataset-specific permissions
[datasets.dispatch_scada]
min_role = "data-analyst"

[datasets.trading_is]
min_role = "data-analyst"

[datasets.rooftopPV_actual]
min_role = "data-analyst"

[datasets.next_day_dispatch]
min_role = "data-engineer"  # Forecasts require higher privilege

[security]
# JWT validation
jwt_required = true
jwt_issuer = "b00t.promptexecution.com"
jwt_audience = "nemweb-mcp"

# Session management
session_timeout_minutes = 60
max_concurrent_sessions = 10
```

### _b00t_.toml (Project Configuration)

```toml
[project]
name = "nemweb-b00t-mcp"
version = "0.2.0"
description = "AEMO nemweb data access for agentic workflows"
homepage = "https://github.com/fungible-farm/nemweb-b00t-mcp"

[b00t]
framework_version = ">=0.1.0"
conformance_level = "full"

[skills]
# Skills provided by this project
provided = ["nemweb", "aemo-data", "dispatch", "trading"]

# Skills required (dependencies)
required = ["python", "sqlite", "bash"]

[mcp]
server_name = "nemweb"
protocol_version = "2024-11-05"

[datums]
# Data storage locations
data_dir = "${HOME}/.b00t/data"
cache_dir = "${HOME}/.b00t/cache/nemweb"
log_dir = "${HOME}/.b00t/logs/nemweb"

[deployment]
container_registry = "ghcr.io/fungible-farm"
container_name = "nemweb-b00t-mcp"
platforms = ["linux/amd64", "linux/arm64"]
```

## justfile (Task Automation)

```just
# nemweb-b00t-mcp justfile

# List available commands
default:
    @just --list

# Install dependencies
install:
    pip install -e .
    cargo build --release -p b00t-mcp-nemweb

# Run all tests
test:
    pytest nemweb/tests/ -v
    cargo test -p b00t-mcp-nemweb

# Start MCP server
serve:
    b00t mcp serve nemweb

# Download sample data for testing
download-sample:
    b00t mcp call nemweb nemweb_download \
        --dataset dispatch_scada \
        --start-date 20240101 \
        --end-date 20240102

# Check data status
status:
    b00t mcp call nemweb nemweb_status

# Update all datasets
update-all:
    b00t mcp call nemweb nemweb_update --all

# Run data quality checks
quality-check:
    b00t mcp call nemweb nemweb_query \
        --sql "SELECT COUNT(*) FROM DISPATCH_UNIT_SCADA WHERE SCADAVALUE IS NULL"

# Clean cache
clean:
    rm -rf ~/.b00t/cache/nemweb/*

# Build documentation
docs:
    cd docs && make html

# Build Docker container
docker-build:
    docker build -t ghcr.io/fungible-farm/nemweb-b00t-mcp:latest .

# Run in container
docker-run:
    docker run --rm -it \
        -v ~/.b00t:/root/.b00t \
        ghcr.io/fungible-farm/nemweb-b00t-mcp:latest

# Run linting
lint:
    black nemweb/
    ruff check nemweb/
    cargo clippy -p b00t-mcp-nemweb

# Format code
format:
    black nemweb/
    cargo fmt -p b00t-mcp-nemweb

# Security scan
security:
    pip-audit
    cargo audit
```

## Integration Checklist

Use this checklist to verify _b00t_ conformance:

### Core Structure
- [ ] `b00t-mcp-nemweb/` directory created
- [ ] `skills/nemweb/` directory created
- [ ] `docs/b00t/` directory created
- [ ] `justfile` created with key recipes
- [ ] `.devcontainer/` configured

### Configuration Files
- [ ] `b00t-mcp.json` with server definition
- [ ] `b00t-mcp-acl.toml` with ACL rules
- [ ] `.mcp.json` for registry
- [ ] `_b00t_.toml` project config
- [ ] `.gitignore` updated for _b00t_ patterns

### MCP Server
- [ ] All 6 core tools implemented
- [ ] Tool discovery working via MCP
- [ ] ACL enforcement functional
- [ ] Error handling with LFMF integration
- [ ] Progress reporting for long operations

### Skills & Documentation
- [ ] Master skill `README-nemweb.md` created
- [ ] Sub-skills documented
- [ ] `b00t learn nemweb` functional
- [ ] LFMF database populated
- [ ] Agent operation guide written

### Testing
- [ ] Unit tests for MCP tools (80%+ coverage)
- [ ] Integration tests for workflows
- [ ] ACL tests
- [ ] Multi-agent coordination tests
- [ ] Performance benchmarks

### CI/CD
- [ ] GitHub Actions workflows configured
- [ ] Container build automation
- [ ] Release automation
- [ ] Security scanning enabled

### Community
- [ ] README updated with _b00t_ integration
- [ ] CONTRIBUTING.md created
- [ ] Example workflows provided
- [ ] Blog post/announcement written

## Next Steps

1. **Review this guide** and the PROJECT_PLAN.md
2. **Set up development environment** with _b00t_ framework installed
3. **Build vertical slice** - Implement nemweb_download tool end-to-end
4. **Iterate** - Refine based on learnings
5. **Complete implementation** following the 10-week plan

## References

- [_b00t_ Main Repository](https://github.com/elasticdotventures/_b00t_)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [Original nemweb Repository](https://github.com/opennem/nemweb)
- [AEMO nemweb Portal](https://nemweb.com.au/)

---

**Version**: 1.0  
**Last Updated**: 2025-11-19  
**Status**: Ready for Implementation
