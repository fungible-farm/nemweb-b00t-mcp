"""
MCP Tool: nemweb_update

Updates all or specific datasets to current date.
Useful for maintaining fresh data.
"""

from typing import Optional, List, Dict
from pathlib import Path
import os
from datetime import datetime, timedelta


def register_update_tool(mcp):
    """Register the nemweb_update tool with the MCP server"""
    
    @mcp.tool()
    def nemweb_update(
        datasets: Optional[List[str]] = None,
        db_name: str = "nemweb.db"
    ) -> Dict[str, any]:
        """
        Update datasets to current date.
        
        Args:
            datasets: List of dataset names to update (optional, defaults to all)
            db_name: Database filename (default: 'nemweb.db')
        
        Returns:
            Dict with updated datasets, records added, and last update time
            
        Example:
            >>> # Update all datasets
            >>> result = nemweb_update()
            >>> print(f"Updated {len(result['updated'])} datasets")
            
            >>> # Update specific datasets
            >>> result = nemweb_update(datasets=['dispatch_scada', 'trading_is'])
        """
        from nemweb import nemweb_current
        
        # Get database path
        data_dir = Path(os.getenv("NEMWEB_DATA_DIR", Path.home() / ".b00t" / "data"))
        db_path = data_dir / db_name
        
        # If no datasets specified, update all
        if datasets is None:
            datasets = list(nemweb_current.DATASETS.keys())
        
        # Validate datasets
        for dataset in datasets:
            if dataset not in nemweb_current.DATASETS:
                raise ValueError(f"Unknown dataset: {dataset}")
        
        # Update each dataset
        handler = nemweb_current.CurrentFileHandler()
        updated = []
        total_records = 0
        
        # Get last 7 days of data to ensure we're current
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        for dataset in datasets:
            try:
                handler.update_data(
                    nemweb_current.DATASETS[dataset],
                    start_date=start_date.strftime("%Y%m%d"),
                    end_date=end_date.strftime("%Y%m%d"),
                    db_name=str(db_path),
                    print_progress=False
                )
                updated.append(dataset)
            except Exception as e:
                # Log error but continue with other datasets
                print(f"Warning: Failed to update {dataset}: {e}")
        
        return {
            'updated': updated,
            'records_added': total_records,
            'last_update': end_date.isoformat(),
            'database': str(db_path)
        }
