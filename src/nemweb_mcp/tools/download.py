"""
MCP Tool: nemweb_download

Downloads AEMO dataset for specified date range and stores in SQLite.
Provides progress reporting for long-running downloads.
"""

from typing import Optional, Dict
from pathlib import Path
import os


def register_download_tool(mcp):
    """Register the nemweb_download tool with the MCP server"""
    
    @mcp.tool()
    def nemweb_download(
        dataset: str,
        start_date: str,
        end_date: Optional[str] = None,
        db_name: str = "nemweb.db"
    ) -> Dict[str, str]:
        """
        Download AEMO dataset for specified date range.
        
        Args:
            dataset: Dataset name (e.g., 'dispatch_scada', 'trading_is')
            start_date: Start date in YYYYMMDD format (e.g., '20240101')
            end_date: End date in YYYYMMDD format (optional, defaults to today)
            db_name: SQLite database filename (default: 'nemweb.db')
        
        Returns:
            Dict with status, dataset, date range, and database path
            
        Example:
            >>> result = nemweb_download(
            ...     dataset='dispatch_scada',
            ...     start_date='20240101',
            ...     end_date='20240131'
            ... )
            >>> print(f"Downloaded to {result['database']}")
        """
        # Import nemweb library directly
        from nemweb import nemweb_current
        from datetime import datetime
        
        # Validate dataset exists
        if dataset not in nemweb_current.DATASETS:
            available = list(nemweb_current.DATASETS.keys())
            raise ValueError(
                f"Unknown dataset '{dataset}'. "
                f"Available datasets: {', '.join(available)}"
            )
        
        # Get data directory
        data_dir = Path(os.getenv("NEMWEB_DATA_DIR", Path.home() / ".b00t" / "data"))
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set database path
        db_path = data_dir / db_name
        
        # Create handler and download data
        handler = nemweb_current.CurrentFileHandler()
        
        # Update data (this is the actual download)
        handler.update_data(
            nemweb_current.DATASETS[dataset],
            start_date=start_date,
            end_date=end_date,
            db_name=str(db_path),
            print_progress=True  # Show progress during download
        )
        
        # Default end_date to today if not specified
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        
        return {
            'status': 'success',
            'dataset': dataset,
            'start_date': start_date,
            'end_date': end_date,
            'database': str(db_path)
        }
