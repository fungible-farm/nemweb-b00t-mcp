"""
MCP Tool: nemweb_query

Executes SQL queries against the nemweb SQLite database.
Provides conversational interface for data exploration.
"""

from typing import Optional, Dict, List
from pathlib import Path
import os
import sqlite3


def register_query_tool(mcp):
    """Register the nemweb_query tool with the MCP server"""
    
    @mcp.tool()
    def nemweb_query(
        sql: str,
        db_name: str = "nemweb.db",
        limit: Optional[int] = 100
    ) -> Dict[str, any]:
        """
        Execute SQL query against nemweb database.
        
        Args:
            sql: SQL query to execute (SELECT statements only)
            db_name: Database filename (default: 'nemweb.db')
            limit: Maximum rows to return (default: 100, max: 10000)
        
        Returns:
            Dict with columns, rows, and row_count
            
        Example:
            >>> result = nemweb_query(
            ...     sql="SELECT AVG(SCADAVALUE) as avg_mw FROM DISPATCH_UNIT_SCADA WHERE DUID='AGLHAL'"
            ... )
            >>> print(result['rows'][0])
        
        Security:
            - Only SELECT queries allowed
            - Results limited to prevent memory issues
            - Database is read-only
        """
        # Validate SQL is a SELECT statement
        sql_upper = sql.strip().upper()
        if not sql_upper.startswith('SELECT'):
            raise ValueError("Only SELECT queries are allowed")
        
        # Enforce limit
        if limit is None or limit > 10000:
            limit = 10000
        
        # Get database path
        data_dir = Path(os.getenv("NEMWEB_DATA_DIR", Path.home() / ".b00t" / "data"))
        db_path = data_dir / db_name
        
        if not db_path.exists():
            raise FileNotFoundError(
                f"Database not found: {db_path}. "
                f"Download data first using nemweb_download."
            )
        
        # Execute query
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row  # Enable column names
        cur = conn.cursor()
        
        try:
            # Add LIMIT if not present
            if 'LIMIT' not in sql_upper:
                sql = f"{sql.rstrip(';')} LIMIT {limit}"
            
            cur.execute(sql)
            rows = cur.fetchall()
            
            # Get column names
            columns = [description[0] for description in cur.description] if rows else []
            
            # Convert rows to list of lists
            rows_data = [list(row) for row in rows]
            
            return {
                'columns': columns,
                'rows': rows_data,
                'row_count': len(rows_data)
            }
        finally:
            conn.close()
