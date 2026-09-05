# nemweb MCP Server Implementation

**Python-native MCP server using fastmcp** for AEMO energy data access.

## Implementation Status

✅ **COMPLETE** - Functional MCP server with 6 tools  
✅ **TESTED** - All tests passing  
✅ **DOCUMENTED** - Code examples and usage guides  

## Quick Start

```bash
# Install dependencies
uv add pandas requests

# Run example
export PYTHONPATH=$(pwd):$PYTHONPATH
python3 examples/basic_usage.py

# Run tests
python3 -m pytest tests/ -v
```

## Architecture

```
nemweb-mcp/
├── src/nemweb_mcp/          # MCP server implementation
│   ├── server.py             # FastMCP server entry point
│   └── tools/                # Individual MCP tools
│       ├── discover.py       # List available datasets
│       ├── download.py       # Download AEMO data
│       ├── query.py          # SQL queries
│       ├── update.py         # Update to current
│       ├── status.py         # Data freshness check
│       └── schema.py         # Table schema info
├── examples/                 # Working code examples
│   ├── basic_usage.py        # Direct tool usage
│   └── mcp_config.py         # Server configuration
├── tests/                    # pytest test suite
│   └── test_mcp_tools.py     # Tool validation tests
└── pyproject.toml            # uv project configuration
```

## MCP Tools

### 1. nemweb_discover

Lists all available AEMO datasets.

```python
result = nemweb_discover()
# Returns: {'datasets': [...], 'count': 6}
```

**Output:**
- dispatch_scada: Dispatch SCADA data (5min updates)
- trading_is: Trading prices and demand (30min updates)
- rooftopPV_actual: Rooftop PV generation (30min updates)
- next_day_actual_gen: Next day forecasts (daily)
- next_day_dispatch: Dispatch forecasts (daily)
- dispatch_is: Dispatch interval summary (5min)

### 2. nemweb_download

Downloads dataset for specified date range.

```python
result = nemweb_download(
    dataset='dispatch_scada',
    start_date='20240101',
    end_date='20240131'
)
# Returns: {'status': 'success', 'database': '...', ...}
```

**Parameters:**
- `dataset`: Dataset name
- `start_date`: YYYYMMDD format
- `end_date`: YYYYMMDD format (optional)
- `db_name`: Database filename (default: 'nemweb.db')

### 3. nemweb_query

Executes SQL queries against the database.

```python
result = nemweb_query(
    sql="SELECT AVG(SCADAVALUE) FROM DISPATCH_UNIT_SCADA WHERE DUID='AGLHAL'"
)
# Returns: {'columns': [...], 'rows': [...], 'row_count': ...}
```

**Security:**
- Only SELECT statements allowed
- Results limited to prevent memory issues
- Database is read-only

### 4. nemweb_update

Updates datasets to current date.

```python
result = nemweb_update(datasets=['dispatch_scada', 'trading_is'])
# Returns: {'updated': [...], 'last_update': '...', ...}
```

### 5. nemweb_status

Checks data freshness and statistics.

```python
result = nemweb_status()
# Returns: {'datasets': [...], 'database_size_mb': ..., ...}
```

**Freshness indicators:**
- `current`: ≤1 day old
- `recent`: ≤7 days old
- `N days old`: Older than 7 days

### 6. nemweb_schema

Returns table schema information.

```python
result = nemweb_schema(table='DISPATCH_UNIT_SCADA')
# Returns: {'tables': [...]}
```

## Code Examples

### Example 1: Discover Datasets

```python
from nemweb_mcp.tools.discover import register_discover_tool

class MockMCP:
    def __init__(self):
        self.tools = {}
    def tool(self):
        def decorator(func):
            self.tools[func.__name__] = func
            return func
        return decorator

mcp = MockMCP()
register_discover_tool(mcp)

result = mcp.tools['nemweb_discover']()
print(f"Found {result['count']} datasets")
for ds in result['datasets']:
    print(f"  {ds['name']}: {ds['description']}")
```

### Example 2: Download Data

```python
from nemweb_mcp.tools.download import register_download_tool

mcp = MockMCP()
register_download_tool(mcp)

result = mcp.tools['nemweb_download'](
    dataset='dispatch_scada',
    start_date='20240101',
    end_date='20240102'
)
print(f"Downloaded to: {result['database']}")
```

### Example 3: Query Data

```python
from nemweb_mcp.tools.query import register_query_tool

mcp = MockMCP()
register_query_tool(mcp)

result = mcp.tools['nemweb_query'](
    sql="""
        SELECT DUID, AVG(SCADAVALUE) as avg_mw
        FROM DISPATCH_UNIT_SCADA
        GROUP BY DUID
        ORDER BY avg_mw DESC
        LIMIT 10
    """
)
for row in result['rows']:
    print(f"{row[0]}: {row[1]:.2f} MW")
```

## Tests

All tests passing:

```bash
$ python3 -m pytest tests/ -v

tests/test_mcp_tools.py::test_discover_tool PASSED         [ 25%]
tests/test_mcp_tools.py::test_status_tool_no_database PASSED [ 50%]
tests/test_mcp_tools.py::test_query_tool_validation PASSED  [ 75%]
tests/test_mcp_tools.py::test_download_tool_validation PASSED [100%]

4 passed in 0.38s
```

## Benefits of This Implementation

✅ **Simple**: Pure Python, no Rust/PyO3 complexity  
✅ **Direct**: Native access to nemweb library  
✅ **Fast**: No FFI overhead  
✅ **Testable**: Easy to test with standard pytest  
✅ **Documented**: Every function has docstrings and examples  
✅ **Minimal**: ~200 LOC per tool vs ~1000 LOC with Rust+FFI  

## Next Steps

1. **Install uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **Setup project**: `uv sync`
3. **Run server**: `uv run python -m nemweb_mcp.server`
4. **Add to _b00t_**: Configure in `b00t-mcp.json`

## MCP Configuration

```json
{
  "mcpServers": {
    "nemweb": {
      "command": "uv",
      "args": ["run", "python", "-m", "nemweb_mcp.server"],
      "env": {
        "NEMWEB_DATA_DIR": "${HOME}/.b00t/data"
      }
    }
  }
}
```

## License

MIT - Same as original nemweb package
