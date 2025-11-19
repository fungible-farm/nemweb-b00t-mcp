# PROJECT PLAN: nemweb-b00t-mcp _b00t_ Conformance Refactoring

## Executive Summary

This project plan outlines the comprehensive refactoring of the nemweb fork to achieve full conformance with the elasticdotventures/_b00t_ framework, transforming it from a standalone Python package into a fully agentic, MCP-integrated tool that can be seamlessly used by AI agents within the _b00t_ ecosystem.

## Background

### Current State
- **Repository**: Fork of opennem/nemweb - Python package for downloading and processing AEMO files
- **Functionality**: Downloads nemweb files and inserts tables into SQLite database
- **Technology**: Python 3.6+, pandas, requests, SQLite
- **Target**: Backend for OpenNEM platform

### Target State (_b00t_ Conformance)
- **Framework Integration**: Full _b00t_ framework conformance with MCP server capabilities
- **Agentic Skills**: Discoverable skills for AI agents to interact with AEMO data
- **Protocol Support**: ACP (Agent Coordination Protocol) for multi-agent workflows
- **Tool Discovery**: MCP tools exposing nemweb functionality to LLM agents
- **Knowledge Base**: Integrated with _b00t_ learn system for tribal knowledge

## _b00t_ Framework Requirements

Based on analysis of elasticdotventures/_b00t_, the following components are required:

### 1. Core Structure
- `b00t-mcp/` - MCP server implementation
- `b00t-cli/` - CLI integration (optional enhancement)
- `skills/` - Skill definitions and templates
- `justfile` - Task automation using casey/just
- `.devcontainer/` - Development container configuration
- `docs/` - _b00t_-style documentation

### 2. Configuration Files
- `b00t-mcp.json` - MCP server configuration
- `b00t-mcp-acl.toml` - Access control list for agent permissions
- `.mcp.json` - MCP registry entry
- `_b00t_.toml` - Project-specific _b00t_ configuration

### 3. MCP Integration
- MCP server exposing nemweb operations as tools
- Tool discovery and capability advertisement
- ACL-controlled access to data operations
- Session management and authentication

### 4. Agentic Skills
- Skill definitions for AEMO data operations
- Templates for common workflows
- Learn system integration
- LFMF (Learn From My Failures) support

## Detailed Implementation Plan

### Sub-Agent Delegation Strategy

To reduce contextual overhead and maximize efficiency, this implementation leverages **parallel sub-agent delegation** throughout all phases. Rather than having a single agent handle all implementation tasks sequentially, we employ specialized code agents (Claude, Codex, etc.) working in parallel on independent modules.

#### Delegation Framework

**Captain Agent (Orchestrator)**
- Coordinates overall project execution
- Assigns tasks to specialized sub-agents
- Validates integration points
- Manages dependencies and timelines
- Focuses on architecture and high-level decisions

**Worker Agents (Specialized Implementers)**
- **Rust MCP Agent**: Implements MCP server, tools, protocol handlers
- **Python Integration Agent**: Creates PyO3 bindings, wraps nemweb library
- **Documentation Agent**: Writes skills, guides, API docs
- **Testing Agent**: Creates unit tests, integration tests, benchmarks
- **DevOps Agent**: Builds CI/CD, containers, deployment automation

#### Parallel Execution Patterns

**Week 1-2: Foundation & MCP Core**
```
Captain: Creates project structure, config templates
  ├─ Worker 1 (Rust): Sets up Cargo project, MCP protocol scaffold
  ├─ Worker 2 (Python): Creates PyO3 bindings, nemweb wrapper
  ├─ Worker 3 (Docs): Writes architecture docs, agent guides
  └─ Worker 4 (DevOps): Sets up devcontainer, justfile recipes

All agents sync at step barrier, integrate components
```

**Week 3-4: Skills & Workflows**
```
Captain: Defines skill structure, workflow patterns
  ├─ Worker 1 (Docs): Creates skill definitions (nemweb, aemo-data, dispatch, trading)
  ├─ Worker 2 (Rust): Implements remaining MCP tools (update, status, schema)
  ├─ Worker 3 (Python): Adds async support, progress reporting
  └─ Worker 4 (Testing): Creates integration test suite

Step barrier: Validate all components work together
```

**Week 5-6: Coordination & Environment**
```
Captain: Designs ACP integration patterns
  ├─ Worker 1 (Rust): Implements ACP message handling, step barriers
  ├─ Worker 2 (Docs): Documents multi-agent patterns, coordination examples
  ├─ Worker 3 (DevOps): Builds Docker images, CI workflows
  └─ Worker 4 (Testing): Creates multi-agent coordination tests

Step barrier: End-to-end workflow validation
```

#### Benefits of Sub-Agent Delegation

✅ **Reduced Context Load**: Each agent focuses on narrow domain, preserves memory  
✅ **Parallel Execution**: 4-5x faster than sequential implementation  
✅ **Specialized Expertise**: Agents leverage domain-specific knowledge (Rust, Python, docs, DevOps)  
✅ **Clear Boundaries**: Minimal context sharing between independent modules  
✅ **Natural Checkpoints**: Step barriers ensure integration points work  

#### Communication & Coordination

- **ACP Step Barriers**: Synchronize agents at phase boundaries
- **Shared Artifacts**: Git repository, configuration files, API contracts
- **Progress Reporting**: Each agent reports status via `b00t acp hive ready`
- **Integration Testing**: Captain validates combined output at each barrier

#### Example: Week 2 Parallel Implementation

```bash
# Captain creates mission for MCP server implementation
b00t acp hive create mcp-server 3 "Implement 6 MCP tools" captain

# Worker 1: Rust agent implements discover, download, query tools
# Worker 2: Python agent creates nemweb wrapper and PyO3 bindings  
# Worker 3: Testing agent writes tool integration tests

# Each worker reports completion
b00t acp hive ready mcp-server 1  # Tools implemented
b00t acp hive sync mcp-server 1   # Wait for all workers

# Captain validates integration
b00t mcp call nemweb nemweb_discover  # Test tool discovery
b00t mcp call nemweb nemweb_download --dataset dispatch_scada --start-date 20240101 --end-date 20240102

# If validation passes, advance to next phase
b00t acp hive ready mcp-server 2
```

### Phase 1: Foundation & Structure (Week 1)

#### 1.1 Directory Structure Setup
- [ ] Initialize project with **uv**: `uv init`
- [ ] Create `src/nemweb_mcp/` for MCP server (Python)
- [ ] Create `skills/nemweb/` for skill definitions
- [ ] Create `docs/b00t/` for _b00t_-specific documentation
- [ ] Add `.devcontainer/` for consistent development environment
- [ ] Create `templates/` for workflow templates
- [ ] Create `superset/` for Apache Superset dashboards

**Files to Create:**
```
nemweb-b00t-mcp/
├── pyproject.toml            # uv project configuration
├── uv.lock                   # uv lockfile
├── src/
│   └── nemweb_mcp/
│       ├── __init__.py
│       ├── server.py         # fastmcp server entry point
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── discover.py   # nemweb_discover tool
│       │   ├── download.py   # nemweb_download tool
│       │   ├── query.py      # nemweb_query tool
│       │   ├── update.py     # nemweb_update tool
│       │   ├── status.py     # nemweb_status tool
│       │   └── schema.py     # nemweb_schema tool
│       └── utils.py          # Helper functions
├── skills/
│   └── nemweb/
│       ├── README-nemweb.md  # Skill documentation
│       ├── aemo-data.md      # AEMO data operations
│       ├── dispatch.md       # Dispatch data workflows
│       └── trading.md        # Trading data workflows
├── superset/
│   ├── dashboards/           # Superset dashboard exports
│   ├── charts/               # Chart definitions
│   └── setup.md              # Superset setup guide
├── templates/
│   └── nemweb/
│       ├── data-pipeline.yaml
│       └── monitoring.yaml
└── docs/
    └── b00t/
        ├── ARCHITECTURE.md
        ├── AGENTS.md         # Agent operation guide
        └── SKILLS.md         # Skill catalog
```

#### 1.2 Configuration Files
- [ ] Create `b00t-mcp.json` with nemweb server definition
- [ ] Create `b00t-mcp-acl.toml` with permissions model
- [ ] Create `.mcp.json` for registry entry
- [ ] Create `_b00t_.toml` for project configuration
- [ ] Update `.gitignore` for _b00t_ patterns

**Configuration Specifications:**

**b00t-mcp.json:**
```json
{
  "servers": {
    "nemweb": {
      "type": "python",
      "module": "b00t_mcp_nemweb.server",
      "description": "AEMO nemweb data access and processing",
      "capabilities": [
        "data_download",
        "sqlite_operations",
        "dispatch_scada",
        "trading_data"
      ]
    }
  }
}
```

**b00t-mcp-acl.toml:**
```toml
[permissions.nemweb]
read_data = ["account.*.data-analyst", "account.*.ai-assistant"]
write_data = ["account.*.data-engineer"]
admin = ["account.engineering.admin"]

[rate_limits]
download_per_hour = 100
query_per_minute = 60
```

#### 1.3 Documentation Foundation
- [ ] Create `docs/b00t/ARCHITECTURE.md` - System architecture
- [ ] Create `docs/b00t/AGENTS.md` - Agent operation guide
- [ ] Create `docs/b00t/SKILLS.md` - Skill catalog
- [ ] Update main `README.md` with _b00t_ integration section
- [ ] Create `CONTRIBUTING.md` following _b00t_ patterns

### Phase 2: MCP Server Implementation (Week 2)

> **Architecture Decision**: Using **fastmcp** (Python-native MCP framework) instead of Rust+PyO3 for simpler, more trivial implementation. _b00t_ is polyglot - Python is first-class.

#### 2.1 MCP Server Core (fastmcp)
- [ ] Set up Python project with **uv** package manager
- [ ] Install fastmcp: `uv add fastmcp`
- [ ] Create MCP server using fastmcp decorators
- [ ] Leverage existing nemweb library directly (no FFI needed)
- [ ] Add error handling and logging
- [ ] Implement session management

**Benefits of fastmcp approach:**
- ✅ **Trivial integration**: Direct Python-to-Python, no language boundaries
- ✅ **Native nemweb access**: Import and use nemweb library directly
- ✅ **Faster development**: No Rust compilation, no PyO3 bindings
- ✅ **Simpler maintenance**: Pure Python codebase
- ✅ **Full _b00t_ polyglot support**: Python is a first-class citizen

**Key MCP Tools to Implement:**
1. **nemweb_discover** - List available datasets
2. **nemweb_download** - Download dataset for date range
3. **nemweb_query** - Query SQLite database
4. **nemweb_update** - Update datasets to current
5. **nemweb_status** - Check data freshness
6. **nemweb_schema** - Get table schema information

#### 2.2 Tool Implementations (fastmcp)
- [ ] Implement `nemweb_discover` tool using @mcp.tool() decorator
- [ ] Implement `nemweb_download` tool with progress reporting
- [ ] Implement `nemweb_query` tool with SQL validation
- [ ] Implement `nemweb_update` tool with concurrent dataset updates
- [ ] Implement `nemweb_status` tool with freshness metrics
- [ ] Implement `nemweb_schema` tool with table introspection

**Tool Specification Example (fastmcp):**
```python
from fastmcp import FastMCP

mcp = FastMCP("nemweb")

@mcp.tool()
def nemweb_download(
    dataset: str,
    start_date: str,
    end_date: str | None = None,
    db_name: str = "nemweb.db"
) -> dict:
    """
    Download AEMO dataset for specified date range.
    
    Args:
        dataset: Dataset name (e.g., 'dispatch_scada', 'trading_is')
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format (optional, defaults to today)
        db_name: SQLite database name (optional)
    
    Returns:
        Dict with status, records_inserted, time_range, database path
    """
    from nemweb import nemweb_current
    
    # Direct access to nemweb library - no FFI, no complexity!
    handler = nemweb_current.CurrentFileHandler()
    handler.update_data(
        nemweb_current.DATASETS[dataset],
        start_date=start_date,
        end_date=end_date,
        db_name=db_name,
        print_progress=True
    )
    
    return {
        "status": "success",
        "dataset": dataset,
        "start_date": start_date,
        "end_date": end_date or "today",
        "database": f"~/.b00t/data/{db_name}"
    }
```

#### 2.3 Project Setup with uv
- [ ] Initialize project with `uv init`
- [ ] Add dependencies: `uv add fastmcp nemweb pandas requests`
- [ ] Create `pyproject.toml` with proper metadata
- [ ] Set up virtual environment: `uv venv`
- [ ] Configure development dependencies: `uv add --dev pytest black ruff`
- [ ] Create MCP server entry point: `src/nemweb_mcp/server.py`

**pyproject.toml structure:**
```toml
[project]
name = "nemweb-mcp"
version = "0.1.0"
description = "AEMO nemweb MCP server for _b00t_ framework"
requires-python = ">=3.12"
dependencies = [
    "fastmcp>=0.1.0",
    "pandas>=2.0.0",
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
```

### Phase 3: Skill System Integration (Week 3)

#### 3.1 Skill Definitions
- [ ] Create `skills/nemweb/README-nemweb.md` master skill document
- [ ] Create AEMO data operations skill templates
- [ ] Create dispatch data workflow documentation
- [ ] Create trading data workflow documentation
- [ ] Add rooftop PV data skill documentation

**Skill Document Structure:**
```markdown
# nemweb Skill: AEMO Data Operations

## Available Tools
- `b00t mcp call nemweb nemweb_discover`
- `b00t mcp call nemweb nemweb_download --dataset dispatch_scada --start-date 20240101`

## Common Workflows

### Download Latest Dispatch Data
\```bash
# Check what datasets are available
b00t mcp call nemweb nemweb_discover

# Download dispatch SCADA for last 7 days
b00t mcp call nemweb nemweb_download \\
  --dataset dispatch_scada \\
  --start-date $(date -d '7 days ago' +%Y%m%d) \\
  --end-date $(date +%Y%m%d)
\```

## LFMF (Learn From My Failures)

Common issues and solutions documented here...
```

#### 3.2 Learn System Integration
- [ ] Create `b00t learn nemweb` template
- [ ] Document available datasets and schemas
- [ ] Add common query patterns
- [ ] Create troubleshooting guide
- [ ] Add performance optimization tips

#### 3.3 LFMF (Learn From My Failures) Setup
- [ ] Set up LFMF data structure for nemweb domain
- [ ] Document common failure patterns
- [ ] Create recovery procedures
- [ ] Add error code documentation

### Phase 4: Task Automation & Workflows (Week 4)

#### 4.1 Justfile Creation
- [ ] Create comprehensive `justfile` for task automation
- [ ] Add installation recipes
- [ ] Add testing recipes
- [ ] Add deployment recipes
- [ ] Add data pipeline recipes

**Justfile Structure:**
```just
# nemweb-b00t-mcp justfile

# Install dependencies and setup environment
install:
    pip install -e .
    b00t-cli install-model nemweb-defaults

# Run tests
test:
    pytest nemweb/tests/

# Download sample data
download-sample:
    b00t mcp call nemweb nemweb_download --dataset dispatch_scada --start-date 20240101 --end-date 20240102

# Update all datasets to current
update-all:
    b00t mcp call nemweb nemweb_update --all

# Check data freshness
status:
    b00t mcp call nemweb nemweb_status

# Start MCP server
serve:
    b00t mcp serve nemweb

# Build documentation
docs:
    cd docs && make html
```

#### 4.2 Workflow Templates
- [ ] Create data download workflow template
- [ ] Create data processing workflow template
- [ ] Create monitoring workflow template
- [ ] Create backup/restore workflow template

### Phase 5: ACP (Agent Coordination Protocol) Support (Week 5)

#### 5.1 Multi-Agent Coordination
- [ ] Implement ACP message handling
- [ ] Add step synchronization for data pipelines
- [ ] Create hive mission templates for multi-agent workflows
- [ ] Add agent discovery for nemweb capabilities

#### 5.2 Coordination Patterns
- [ ] Implement captain-worker pattern for data downloads
- [ ] Add voting mechanism for data quality checks
- [ ] Create task delegation for parallel processing
- [ ] Add progress reporting across agents

**Example Coordination:**
```rust
// Captain agent coordinates multiple workers downloading different datasets
async fn coordinate_data_download(mission_id: &str) {
    // Create mission with 3 workers
    hive_create_mission(mission_id, 3, "Download Q1 2024 data").await;
    
    // Workers join and take tasks
    // Worker 1: dispatch_scada
    // Worker 2: trading_is
    // Worker 3: rooftop_pv
    
    // Synchronize at step 1: all downloads complete
    hive_sync(mission_id, 1).await;
    
    // Step 2: Data validation
    hive_sync(mission_id, 2).await;
    
    // Step 3: Load into database
    hive_sync(mission_id, 3).await;
}
```

### Phase 6: Development Environment (Week 6)

#### 6.1 DevContainer Setup
- [ ] Create `.devcontainer/devcontainer.json`
- [ ] Add required Python and Rust toolchains
- [ ] Include _b00t_ framework installation
- [ ] Configure VSCode extensions
- [ ] Add MCP server configuration

**devcontainer.json:**
```json
{
  "name": "nemweb-b00t-mcp",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "features": {
    "ghcr.io/devcontainers/features/rust:1": {},
    "ghcr.io/devcontainers/features/node:1": {}
  },
  "postCreateCommand": "pip install -e . && cargo build --release",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "rust-lang.rust-analyzer",
        "skellock.just"
      ],
      "settings": {
        "mcp.servers": {
          "nemweb": {
            "command": "b00t",
            "args": ["mcp", "serve", "nemweb"]
          }
        }
      }
    }
  }
}
```

#### 6.2 Docker Support
- [ ] Create `Dockerfile` for containerized deployment
- [ ] Create `docker-compose.yml` for development
- [ ] Add container build workflow
- [ ] Create deployment scripts

### Phase 7: Testing & Quality (Week 7)

#### 7.1 Test Infrastructure
- [ ] Set up pytest for Python tests
- [ ] Add cargo test for Rust components
- [ ] Create integration tests for MCP tools
- [ ] Add end-to-end workflow tests
- [ ] Implement test data fixtures

#### 7.2 Test Coverage
- [ ] Unit tests for all MCP tools (target: 80%+)
- [ ] Integration tests for workflows
- [ ] Performance benchmarks
- [ ] Security tests for ACL enforcement
- [ ] Compatibility tests across Python versions

#### 7.3 Quality Assurance
- [ ] Set up pre-commit hooks
- [ ] Add linting (black, ruff for Python; clippy for Rust)
- [ ] Configure mypy for type checking
- [ ] Add code formatting checks
- [ ] Implement CI/CD pipeline

### Phase 8: CI/CD & Automation (Week 8)

#### 8.1 GitHub Actions Workflows
- [ ] Create test workflow (runs on PR)
- [ ] Create build workflow (builds artifacts)
- [ ] Create release workflow (publishes packages)
- [ ] Add container build and push workflow
- [ ] Implement security scanning

**Example Workflow:**
```yaml
name: Test and Build

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup _b00t_
        run: curl -fsSL https://raw.githubusercontent.com/elasticdotventures/_b00t_/main/install.sh | sh
      - name: Run tests
        run: just test
      
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build MCP server
        run: cargo build --release -p b00t-mcp-nemweb
```

#### 8.2 Release Automation
- [ ] Set up semantic versioning
- [ ] Configure cocogitto for changelog generation
- [ ] Add release tagging automation
- [ ] Create package publishing workflow

### Phase 9: Documentation & Knowledge Base (Week 9)

#### 9.1 Comprehensive Documentation
- [ ] Complete API documentation
- [ ] Add usage examples for each tool
- [ ] Create tutorial series
- [ ] Add troubleshooting guide
- [ ] Write migration guide from original nemweb

#### 9.2 Agentic Documentation
- [ ] Create agent-friendly documentation format
- [ ] Add skill-based navigation
- [ ] Include contextual examples
- [ ] Add tribal knowledge database
- [ ] Create quick reference cards

#### 9.3 Video & Interactive Content
- [ ] Create demo videos
- [ ] Add interactive examples
- [ ] Build sample workflows
- [ ] Create Jupyter notebooks for data science workflows

### Phase 10: Community & Ecosystem (Week 10)

#### 10.1 Integration Examples
- [ ] Create example agent workflows
- [ ] Add integration with other _b00t_ tools
- [ ] Build sample data pipelines
- [ ] Create monitoring dashboards

#### 10.2 Data Visualization & Analytics
- [ ] Set up **Apache Superset** for data visualization
- [ ] Create Superset dashboards for AEMO data
- [ ] Configure data sources (SQLite connection)
- [ ] Build example visualizations:
  - Dispatch SCADA time series
  - Regional price heatmaps
  - Generation unit performance
  - Rooftop PV forecasts vs actuals
- [ ] Document Superset setup in skills

**Apache Superset Integration:**
```bash
# Install Superset via uv
uv add apache-superset

# Initialize Superset database
superset db upgrade

# Create admin user
superset fab create-admin

# Load example dashboards
superset init

# Connect to nemweb SQLite database
# Dashboard: "AEMO Real-Time Dispatch"
# - Chart 1: Dispatch prices by region (last 24h)
# - Chart 2: Generation by fuel type
# - Chart 3: Demand vs forecast
```

**MCP Chat Interface:**
- MCP provides conversational interface for data queries
- Agents can ask: "What was the average dispatch price in NSW yesterday?"
- Superset provides visual exploration and dashboards
- Both interfaces work together: chat for quick queries, dashboards for analysis

#### 10.3 Community Building
- [ ] Write blog post announcing _b00t_ integration
- [ ] Create contribution guide
- [ ] Set up discussions forum
- [ ] Add code of conduct
- [ ] Create issue templates

## Technical Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent (Claude, etc.)                   │
│                   - Chat Interface (MCP)                     │
│                   - Conversational Queries                   │
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Protocol
┌────────────────────────▼────────────────────────────────────┐
│                  b00t MCP Framework                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  nemweb MCP Server (fastmcp - Python)                │   │
│  │  - Tool Discovery (@mcp.tool decorators)             │   │
│  │  - Tool Execution (direct Python calls)              │   │
│  │  - ACL Enforcement                                    │   │
│  │  - Session Management                                 │   │
│  │  - Native nemweb integration (no FFI!)               │   │
│  └─────────────────────┬────────────────────────────────┘   │
└────────────────────────┼────────────────────────────────────┘
                         │ Direct Python import
┌────────────────────────▼────────────────────────────────────┐
│           Python nemweb Library (existing)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  - CurrentFileHandler                                 │   │
│  │  - Dataset Management                                 │   │
│  │  - SQLite Operations                                  │   │
│  │  - File Download & Processing                         │   │
│  └─────────────────────┬────────────────────────────────┘   │
└────────────────────────┼────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌──────────────────────┐    ┌──────────────────────────┐
│  nemweb.com.au       │    │  SQLite Database         │
│  (AEMO data source)  │    │  (local storage)         │
└──────────────────────┘    └───────────┬──────────────┘
                                        │
                            ┌───────────▼──────────────┐
                            │  Apache Superset         │
                            │  - Dashboards            │
                            │  - Visualizations        │
                            │  - Analytics             │
                            └──────────────────────────┘
```

### Data Flow

1. **Agent Request**: AI agent discovers nemweb capabilities via MCP
2. **Tool Invocation**: Agent calls MCP tool (e.g., nemweb_download)
3. **ACL Check**: b00t framework validates permissions
4. **Execution**: fastmcp server calls nemweb library directly (same Python process)
5. **Data Processing**: nemweb downloads and processes AEMO data
6. **Storage**: Data stored in SQLite database
7. **Response**: Results returned to agent via MCP protocol
8. **Visualization**: Superset provides dashboards and analytics (optional)

**Key Simplifications with fastmcp:**
- ✅ No Rust compilation required
- ✅ No PyO3 FFI complexity
- ✅ Direct Python-to-Python calls (same process)
- ✅ Faster development and iteration
- ✅ Easier debugging (all Python stack traces)

## Success Criteria

### Functional Requirements
- ✅ All existing nemweb functionality preserved
- ✅ MCP server exposes all core operations as tools
- ✅ ACL system enforces permissions correctly
- ✅ Skills are discoverable via `b00t learn nemweb`
- ✅ Multi-agent coordination works via ACP
- ✅ Documentation follows _b00t_ patterns

### Non-Functional Requirements
- ✅ Test coverage > 80%
- ✅ API response time < 100ms for queries
- ✅ Download operations support progress reporting
- ✅ Error messages are actionable and logged to LFMF
- ✅ Container build < 5 minutes
- ✅ Installation via `b00t install nemweb` works

### Agent Experience
- ✅ Agent can discover nemweb capabilities without documentation
- ✅ Agent can download data with single tool call
- ✅ Agent can coordinate multi-dataset downloads across workers
- ✅ Agent receives clear error messages with recovery suggestions
- ✅ Agent can learn from past failures via LFMF system

## Risk Assessment

### Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| PyO3 interop complexity | High | Medium | Start with simple bindings, iterate |
| Performance overhead from Rust<->Python | Medium | Medium | Benchmark early, optimize hot paths |
| MCP protocol changes | Medium | Low | Pin to stable MCP version, test compatibility |
| SQLite concurrency issues | High | Medium | Use WAL mode, implement connection pooling |

### Schedule Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| Underestimated complexity | High | Medium | Build vertical slice first, adjust estimates |
| Dependency on _b00t_ updates | Medium | Low | Use stable _b00t_ APIs, avoid bleeding edge |
| Testing takes longer than planned | Medium | High | Start testing early, automate thoroughly |

## Dependencies

### External Dependencies
- elasticdotventures/_b00t_ framework (latest stable)
- **uv** - Modern Python package manager (required)
- Python 3.12+
- SQLite 3.35+
- pandas, requests (existing dependencies)

### New Dependencies (Python - via uv)
- **fastmcp** - Python-native MCP framework (primary)
- **apache-superset** - Data visualization and analytics
- pytest - Testing framework
- black - Code formatting
- ruff - Linting
- casey/just - Task automation (optional, can use uv scripts)

**Installation:**
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize project
uv init

# Add core dependencies
uv add fastmcp pandas requests

# Add visualization
uv add apache-superset

# Add development dependencies
uv add --dev pytest black ruff
```

## Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| 1. Foundation | Week 1 | Directory structure, config files, docs foundation, uv setup |
| 2. MCP Server | Week 2 | fastmcp server with 6 core tools (Python-native) |
| 3. Skills | Week 3 | Skill definitions, learn integration, LFMF setup |
| 4. Workflows | Week 4 | Justfile/uv scripts, workflow templates |
| 5. ACP | Week 5 | Multi-agent coordination support |
| 6. DevEnv | Week 6 | DevContainer, Docker setup |
| 7. Testing | Week 7 | Comprehensive test suite |
| 8. CI/CD | Week 8 | Automated workflows |
| 9. Docs | Week 9 | Complete documentation |
| 10. Community | Week 10 | Integration examples, Apache Superset dashboards |

**Total Duration**: 10 weeks (2.5 months) sequential / **6-7 weeks with sub-agent parallelization**

## Resource Requirements

### Personnel (Sub-Agent Delegation Model)

**Captain Agent (Primary Orchestrator)**
- 1 Senior Architect/Tech Lead
- Coordinates sub-agents across all phases
- Validates integration points
- Manages timelines and dependencies
- Reduced context load: focuses on high-level coordination vs. implementation details

**Worker Agents (Specialized Code Agents)**
- 1 Python/fastmcp Specialist Agent (Claude/Codex specialized for Python)
  - fastmcp MCP server implementation
  - Tool decorators and implementations
  - Direct nemweb library integration (no FFI)
  - Async support and progress reporting
  
- 1 Data Visualization Agent (Claude/Codex specialized for analytics)
  - Apache Superset setup and configuration
  - Dashboard creation
  - SQLite data source integration
  - Chart and visualization design
  
- 1 Documentation Agent (Claude/Codex specialized for technical writing)
  - Skills documentation
  - API references
  - Agent operation guides
  
- 1 Testing & QA Agent (Claude/Codex specialized for testing)
  - Unit tests (pytest), integration tests
  - Performance benchmarks
  - Security testing
  
- 1 DevOps Agent (part-time, Claude/Codex specialized for infrastructure)
  - CI/CD pipelines
  - Container builds
  - uv-based deployment automation

**Benefits of Sub-Agent Model with fastmcp:**
- ✅ **4-5x faster execution** through parallelization
- ✅ **Simpler stack** - all Python, no Rust compilation or FFI
- ✅ **Lower cognitive overhead** - each agent has narrow, specialized context
- ✅ **Better quality** - agents leverage domain-specific expertise
- ✅ **Natural checkpoints** - ACP step barriers ensure integration
- ✅ **Reduced timeline** - 10 weeks → potentially 6-7 weeks with parallel execution
- ✅ **Trivial integration** - Python agents working in Python (no language boundaries)

### Infrastructure
- GitHub Actions minutes for CI/CD
- Container registry storage
- Test infrastructure for integration tests

## Next Steps

1. **Review & Approval**: Get stakeholder sign-off on this plan
2. **Environment Setup**: Set up development environment with _b00t_ framework
3. **Vertical Slice**: Build one complete feature (e.g., nemweb_download tool) end-to-end
4. **Iteration**: Refine estimates based on vertical slice learnings
5. **Execute**: Begin Phase 1 implementation

## Appendices

### A. _b00t_ Framework Reference
- Main repository: https://github.com/elasticdotventures/_b00t_
- MCP specification: https://modelcontextprotocol.io/
- ACP documentation: See _b00t_ b00t_overview.md

### B. AEMO Data Reference
- nemweb.com.au data structure
- Available datasets and schemas
- Update frequency and schedules

### C. Original nemweb Documentation
- Current README and setup instructions
- API documentation
- Testing approach

---

**Document Version**: 1.0
**Last Updated**: 2025-11-19
**Status**: Draft - Pending Review
**Authors**: Copilot Agent
**Reviewers**: TBD
