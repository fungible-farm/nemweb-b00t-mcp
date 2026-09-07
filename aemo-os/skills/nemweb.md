# Skill: nemweb

Using the nemweb MCP server to access AEMO energy market data.

## MCP Tools Available

### nemweb_discover
List all available AEMO datasets.

```bash
b00t mcp call nemweb nemweb_discover
```

Returns datasets with metadata:
- dispatch_scada: 5-min generation data
- trading_is: 30-min prices and demand
- rooftopPV_actual: Rooftop solar generation
- dispatch_is: Dispatch interval summaries

### nemweb_download
Download dataset for date range.

```bash
b00t mcp call nemweb nemweb_download \
  --dataset dispatch_scada \
  --start-date 20240101 \
  --end-date 20240131
```

### nemweb_query
Execute SQL queries against stored data.

```bash
b00t mcp call nemweb nemweb_query \
  --sql "SELECT AVG(SCADAVALUE) FROM DISPATCH_UNIT_SCADA WHERE DUID='AGLHAL'"
```

### nemweb_status
Check data freshness and statistics.

```bash
b00t mcp call nemweb nemweb_status
```

### nemweb_update
Update datasets to current.

```bash
b00t mcp call nemweb nemweb_update \
  --datasets dispatch_scada,trading_is
```

### nemweb_schema
Get table schema information.

```bash
b00t mcp call nemweb nemweb_schema \
  --table DISPATCH_UNIT_SCADA
```

## Common Workflows

### 1. Initial Data Download

```bash
# Discover available datasets
b00t mcp call nemweb nemweb_discover

# Download dispatch SCADA for last 30 days
b00t mcp call nemweb nemweb_download \
  --dataset dispatch_scada \
  --start-date $(date -d '30 days ago' +%Y%m%d) \
  --end-date $(date +%Y%m%d)

# Check status
b00t mcp call nemweb nemweb_status
```

### 2. Query Analysis

```bash
# Get schema
b00t mcp call nemweb nemweb_schema --table DISPATCH_UNIT_SCADA

# Run analysis query
b00t mcp call nemweb nemweb_query --sql "
  SELECT 
    DUID,
    AVG(SCADAVALUE) as avg_mw,
    MAX(SCADAVALUE) as peak_mw
  FROM DISPATCH_UNIT_SCADA
  GROUP BY DUID
  ORDER BY avg_mw DESC
  LIMIT 20
"
```

### 3. Daily Updates

```bash
# Update all datasets
b00t mcp call nemweb nemweb_update

# Check freshness
b00t mcp call nemweb nemweb_status
```

## Tips

- Use `--start-date` and `--end-date` in YYYYMMDD format
- SQL queries are SELECT-only for security
- Results are limited to 100 rows by default (use LIMIT to change)
- Data is stored in `~/.b00t/data/nemweb.db`
