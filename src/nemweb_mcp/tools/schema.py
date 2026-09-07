"""
MCP Tool: nemweb_schema

Returns database schema information for tables.
Useful for understanding data structure and writing queries.
"""

from typing import Optional, Dict, List
from pathlib import Path
import os
import sqlite3


def register_schema_tool(mcp):
    """Register the nemweb_schema tool with the MCP server"""
    
    @mcp.tool()
    def nemweb_schema(
        table: Optional[str] = None,
        db_name: str = "nemweb.db"
    ) -> Dict[str, any]:
        """
        Get table schema information.
        
        Args:
            table: Specific table name (optional, returns all if not specified)
            db_name: Database filename (default: 'nemweb.db')
        
        Returns:
            Dict with table schemas including column names and types
            
        Example:
            >>> # Get all table schemas
            >>> result = nemweb_schema()
            >>> for tbl in result['tables']:
            ...     print(f"{tbl['name']}: {len(tbl['columns'])} columns")
            
            >>> # Get specific table schema
            >>> result = nemweb_schema(table='DISPATCH_UNIT_SCADA')
            >>> print(result['tables'][0]['columns'])
        """
        # Get database path
        data_dir = Path(os.getenv("NEMWEB_DATA_DIR", Path.home() / ".b00t" / "data"))
        db_path = data_dir / db_name
        
        if not db_path.exists():
            raise FileNotFoundError(
                f"Database not found: {db_path}. "
                f"Download data first using nemweb_download."
            )
        
        # Connect to database
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        
        # Get tables to describe
        if table:
            tables = [table]
        else:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cur.fetchall()]
        
        schemas = []
        
        for tbl in tables:
            # Get table info
            cur.execute(f"PRAGMA table_info({tbl})")
            columns_info = cur.fetchall()
            
            # Get row count
            cur.execute(f"SELECT COUNT(*) FROM {tbl}")
            row_count = cur.fetchone()[0]
            
            # Format column information
            columns = [
                {
                    'name': col[1],
                    'type': col[2],
                    'nullable': not col[3],
                    'primary_key': bool(col[5])
                }
                for col in columns_info
            ]
            
            schemas.append({
                'name': tbl,
                'columns': columns,
                'row_count': row_count
            })
        
        conn.close()
        
        return {
            'tables': schemas,
            'database': str(db_path)
        }
