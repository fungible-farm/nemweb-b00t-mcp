"""
MCP Tool: nemweb_status

Checks data freshness and provides database statistics.
Useful for monitoring data quality and coverage.
"""

from typing import Dict, List
from pathlib import Path
import os
import sqlite3


def register_status_tool(mcp):
    """Register the nemweb_status tool with the MCP server"""
    
    @mcp.tool()
    def nemweb_status(db_name: str = "nemweb.db") -> Dict[str, any]:
        """
        Check data freshness and database statistics.
        
        Args:
            db_name: Database filename (default: 'nemweb.db')
        
        Returns:
            Dict with dataset statistics including latest date, record count, and size
            
        Example:
            >>> result = nemweb_status()
            >>> for dataset in result['datasets']:
            ...     print(f"{dataset['name']}: {dataset['record_count']} records")
        """
        # Get database path
        data_dir = Path(os.getenv("NEMWEB_DATA_DIR", Path.home() / ".b00t" / "data"))
        db_path = data_dir / db_name
        
        if not db_path.exists():
            return {
                'exists': False,
                'database_path': str(db_path),
                'message': 'Database not found. Download data using nemweb_download.'
            }
        
        # Get database size
        db_size_mb = db_path.stat().st_size / (1024 * 1024)
        
        # Connect and get table statistics
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        
        datasets = []
        
        # Common tables and their associated datasets
        table_dataset_map = {
            'DISPATCH_UNIT_SCADA': 'dispatch_scada',
            'TRADING_PRICE': 'trading_is',
            'TRADING_REGIONSUM': 'trading_is',
            'ROOFTOP_PV_ACTUAL': 'rooftopPV_actual',
            'NEXT_DAY_ACTUAL_GEN': 'next_day_actual_gen',
            'NEXT_DAY_DISPATCH': 'next_day_dispatch',
            'DISPATCH_PRICE': 'dispatch_is',
            'DISPATCH_REGIONSUM': 'dispatch_is'
        }
        
        # Get list of tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cur.fetchall()]
        
        for table in tables:
            if table in table_dataset_map:
                # Get record count
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                record_count = cur.fetchone()[0]
                
                # Get date range
                try:
                    cur.execute(f"SELECT MIN(SETTLEMENTDATE), MAX(SETTLEMENTDATE) FROM {table}")
                    min_date, max_date = cur.fetchone()
                    latest_date = max_date if max_date else "N/A"
                    
                    # Determine freshness
                    from datetime import datetime, timedelta
                    if max_date:
                        latest_dt = datetime.strptime(max_date[:10], "%Y-%m-%d")
                        days_old = (datetime.now() - latest_dt).days
                        if days_old <= 1:
                            freshness = "current"
                        elif days_old <= 7:
                            freshness = "recent"
                        else:
                            freshness = f"{days_old} days old"
                    else:
                        freshness = "unknown"
                except:
                    latest_date = "N/A"
                    freshness = "unknown"
                
                datasets.append({
                    'name': table_dataset_map[table],
                    'table': table,
                    'latest_date': latest_date,
                    'record_count': record_count,
                    'freshness': freshness
                })
        
        conn.close()
        
        return {
            'exists': True,
            'datasets': datasets,
            'database_size_mb': round(db_size_mb, 2),
            'database_path': str(db_path)
        }
