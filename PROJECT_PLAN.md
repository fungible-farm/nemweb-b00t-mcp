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

### Phase 1: Foundation & Structure (Week 1)

#### 1.1 Directory Structure Setup
- [ ] Create `b00t-mcp-nemweb/` directory for MCP server
- [ ] Create `skills/nemweb/` for skill definitions
- [ ] Create `docs/b00t/` for _b00t_-specific documentation
- [ ] Add `.devcontainer/` for consistent development environment
- [ ] Create `templates/` for workflow templates

**Files to Create:**
```
nemweb-b00t-mcp/
├── b00t-mcp-nemweb/          # MCP server implementation
│   ├── src/
│   │   ├── main.rs           # MCP server entry point
│   │   ├── tools/            # MCP tool implementations
│   │   ├── nemweb_client.py  # Python binding to nemweb
│   │   └── lib.rs
│   ├── Cargo.toml
│   └── README.md
├── skills/
│   └── nemweb/
│       ├── README-nemweb.md  # Skill documentation
│       ├── aemo-data.md      # AEMO data operations
│       ├── dispatch.md       # Dispatch data workflows
│       └── trading.md        # Trading data workflows
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

#### 2.1 MCP Server Core
- [ ] Set up Rust project structure for MCP server
- [ ] Implement MCP protocol handlers (tools/list, tools/call)
- [ ] Create Python interop layer for nemweb library
- [ ] Add error handling and logging
- [ ] Implement session management

**Key MCP Tools to Implement:**
1. **nemweb_discover** - List available datasets
2. **nemweb_download** - Download dataset for date range
3. **nemweb_query** - Query SQLite database
4. **nemweb_update** - Update datasets to current
5. **nemweb_status** - Check data freshness
6. **nemweb_schema** - Get table schema information

#### 2.2 Tool Implementations
- [ ] Implement `nemweb_discover` tool
- [ ] Implement `nemweb_download` tool
- [ ] Implement `nemweb_query` tool
- [ ] Implement `nemweb_update` tool
- [ ] Implement `nemweb_status` tool
- [ ] Implement `nemweb_schema` tool

**Tool Specification Example:**
```rust
#[derive(derive_mcp::Tool)]
struct NemwebDownload {
    /// Dataset name (e.g., 'dispatch_scada', 'trading_is')
    dataset: String,
    /// Start date in YYYYMMDD format
    start_date: String,
    /// End date in YYYYMMDD format (optional)
    end_date: Option<String>,
    /// SQLite database name (optional, defaults to 'nemweb.db')
    db_name: Option<String>,
}
```

#### 2.3 Python Integration Layer
- [ ] Create Python module `b00t_mcp_nemweb`
- [ ] Implement PyO3 bindings for Rust<->Python interop
- [ ] Wrap existing nemweb functions for MCP access
- [ ] Add async support for long-running operations
- [ ] Implement progress reporting

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

#### 10.2 Community Building
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
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Protocol
┌────────────────────────▼────────────────────────────────────┐
│                  b00t MCP Framework                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  nemweb MCP Server (Rust)                            │   │
│  │  - Tool Discovery                                     │   │
│  │  - Tool Execution                                     │   │
│  │  - ACL Enforcement                                    │   │
│  │  - Session Management                                 │   │
│  └─────────────────────┬────────────────────────────────┘   │
└────────────────────────┼────────────────────────────────────┘
                         │ PyO3 FFI
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
┌────────────────────────▼────────────────────────────────────┐
│                   External Services                          │
│  - nemweb.com.au (AEMO data source)                         │
│  - SQLite Database (local storage)                          │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Agent Request**: AI agent discovers nemweb capabilities via MCP
2. **Tool Invocation**: Agent calls MCP tool (e.g., nemweb_download)
3. **ACL Check**: b00t framework validates permissions
4. **Execution**: Rust server calls Python nemweb library via PyO3
5. **Data Processing**: nemweb downloads and processes AEMO data
6. **Storage**: Data stored in SQLite database
7. **Response**: Results returned to agent via MCP protocol

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
- Rust 1.82+ with cargo
- Python 3.12+
- SQLite 3.35+
- pandas, requests (existing dependencies)

### New Dependencies
- PyO3 for Rust<->Python interop
- derive_mcp for MCP tool generation
- tokio for async runtime
- serde for serialization
- casey/just for task automation

## Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| 1. Foundation | Week 1 | Directory structure, config files, docs foundation |
| 2. MCP Server | Week 2 | Working MCP server with 6 core tools |
| 3. Skills | Week 3 | Skill definitions, learn integration, LFMF setup |
| 4. Workflows | Week 4 | Justfile, workflow templates |
| 5. ACP | Week 5 | Multi-agent coordination support |
| 6. DevEnv | Week 6 | DevContainer, Docker setup |
| 7. Testing | Week 7 | Comprehensive test suite |
| 8. CI/CD | Week 8 | Automated workflows |
| 9. Docs | Week 9 | Complete documentation |
| 10. Community | Week 10 | Integration examples, community setup |

**Total Duration**: 10 weeks (2.5 months)

## Resource Requirements

### Personnel
- 1 Senior Engineer (Rust + Python expertise)
- 1 DevOps Engineer (part-time for CI/CD)
- 1 Technical Writer (part-time for documentation)

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
