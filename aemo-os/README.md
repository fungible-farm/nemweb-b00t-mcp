# AEMO Operating System (aemo-os)

**Complete AEMO analysis environment with tools, agents, skills, and webserver.**

## What is AEMO OS?

AEMO OS is a bootstrap system that discovers, installs, and configures everything needed to analyze the National Electricity Market (NEM):

- **Tools**: nemweb MCP server, database clients, visualization
- **Agents**: AI agents for data processing and analysis
- **Skills**: AEMO domain knowledge and workflows  
- **Webserver**: Vue3 frontend for interactive exploration
- **Databases**: SQLite data warehouse for AEMO data

## Quick Start

```bash
# Run bootstrap
python3 aemo-os/aemos.py

# Discover what will be installed
python3 aemo-os/aemos.py --discover
```

## What Gets Installed

### 1. Tools

- **uv**: Modern Python package manager
- **nemweb-mcp**: MCP server for AEMO data access
- **Node.js**: For Vue3 webserver (optional)

### 2. Agents

- **nemweb_agent**: Processes AEMO data, downloads datasets
- **visualization_agent**: Creates charts and dashboards
- **analysis_agent**: Market analysis and forecasting

### 3. Skills

Located in `aemo-os/skills/`:

- `nemweb.md` - Using the nemweb MCP server
- `aemo-data.md` - AEMO data structures and schemas
- `dispatch.md` - Dispatch process and SCADA data
- `trading.md` - Trading intervals and pricing

### 4. Databases

- **nemweb.db**: SQLite database at `~/.b00t/data/nemweb.db`
  - AEMO data warehouse
  - Tables for dispatch, trading, rooftop PV, forecasts

### 5. Webserver

Vue3 single-page application at `aemo-os/webserver/`:

- Dataset explorer
- SQL query interface  
- Database status monitoring
- Agent chat interface (future)

**Port**: 8080

## Usage

### Bootstrap System

```bash
# Full bootstrap
python3 aemo-os/aemos.py

# Discovery only
python3 aemo-os/aemos.py --discover
```

### Start Webserver

```bash
# Simple (no build)
cd aemo-os/webserver
python3 -m http.server 8080

# Open browser
open http://localhost:8080
```

### Download AEMO Data

```bash
# Using MCP tools
export PYTHONPATH=$(pwd):$PYTHONPATH
python3 -c "
from nemweb_mcp.tools.download import register_download_tool
from nemweb_mcp.tools.discover import register_discover_tool

class MockMCP:
    def __init__(self):
        self.tools = {}
    def tool(self):
        return lambda f: (self.tools.update({f.__name__: f}), f)[1]

mcp = MockMCP()
register_discover_tool(mcp)
register_download_tool(mcp)

# Discover datasets
result = mcp.tools['nemweb_discover']()
print(f\"Found {result['count']} datasets\")

# Download sample data (requires network)
# result = mcp.tools['nemweb_download'](
#     dataset='dispatch_scada',
#     start_date='20240101',
#     end_date='20240102'
# )
"
```

### Query Data

```bash
# Using MCP tools
python3 -c "
from nemweb_mcp.tools.query import register_query_tool

class MockMCP:
    def __init__(self):
        self.tools = {}
    def tool(self):
        return lambda f: (self.tools.update({f.__name__: f}), f)[1]

mcp = MockMCP()
register_query_tool(mcp)

# Execute query (requires downloaded data)
# result = mcp.tools['nemweb_query'](
#     sql='SELECT COUNT(*) FROM DISPATCH_UNIT_SCADA'
# )
# print(result)
"
```

## Directory Structure

```
aemo-os/
├── README.md              # This file
├── aemos.py               # Bootstrap script
├── config/
│   └── agents.json        # Agent configuration
├── skills/
│   ├── nemweb.md          # nemweb skill
│   ├── aemo-data.md       # AEMO data skill
│   ├── dispatch.md        # Dispatch skill
│   └── trading.md         # Trading skill
├── webserver/
│   ├── index.html         # Vue3 SPA
│   └── package.json       # Node.js config
└── scripts/
    └── bootstrap.sh       # Shell bootstrap (future)
```

## Architecture

```
User/Agent
    ↓
Vue3 Webserver (Port 8080)
    ↓
MCP Server (nemweb_mcp)
    ↓
SQLite Database (~/.b00t/data/nemweb.db)
    ↓
AEMO Data
```

## Features

### Dataset Explorer

Browse all available AEMO datasets:
- Dispatch SCADA (5-min generation data)
- Trading Interval Summary (30-min prices)
- Rooftop PV actual generation
- Dispatch forecasts

### SQL Query Interface

Execute queries directly from the web interface:
```sql
SELECT 
    DUID,
    AVG(SCADAVALUE) as avg_mw
FROM DISPATCH_UNIT_SCADA
WHERE SETTLEMENTDATE >= '2024-01-01'
GROUP BY DUID
ORDER BY avg_mw DESC
LIMIT 10
```

### Database Status

Monitor data freshness and coverage:
- Latest data timestamp
- Record counts per dataset
- Database size

### Agent Integration

Connect AI agents to analyze NEM data:
- Conversational queries
- Automated analysis
- Report generation

## Configuration

### Agent Configuration

Edit `aemo-os/config/agents.json`:

```json
{
  "agents": {
    "nemweb_agent": {
      "skills": ["nemweb", "aemo-data"]
    },
    "visualization_agent": {
      "skills": ["superset", "charts"]
    }
  }
}
```

### MCP Server

The nemweb MCP server is located at `src/nemweb_mcp/`.

Start it with:
```bash
export PYTHONPATH=$(pwd):$PYTHONPATH
python3 -m src.nemweb_mcp.server
```

## Next Steps

1. **Download Data**: Use MCP tools to download AEMO datasets
2. **Explore Web UI**: Open http://localhost:8080 after starting webserver
3. **Run Queries**: Use SQL interface to analyze data
4. **Connect Agents**: Configure AI agents to use MCP server

## Requirements

- Python 3.12+
- pandas, requests (installed by bootstrap)
- Node.js (optional, for advanced webserver features)

## License

MIT - Same as nemweb package
