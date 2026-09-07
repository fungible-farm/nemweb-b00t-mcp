"""
MCP Tool: nemweb_discover

Discovers available AEMO datasets that can be downloaded via nemweb.
Returns metadata about each dataset including update frequency and tables.
"""

from typing import Dict, List


def register_discover_tool(mcp):
    """Register the nemweb_discover tool with the MCP server"""
    
    @mcp.tool()
    def nemweb_discover() -> Dict[str, List[Dict[str, str]]]:
        """
        List all available AEMO nemweb datasets.
        
        Returns:
            Dict with 'datasets' key containing list of dataset metadata:
            - name: Dataset identifier
            - description: Human-readable description
            - update_frequency: How often data is updated
            - tables: List of SQLite tables created
            
        Example:
            >>> result = nemweb_discover()
            >>> for dataset in result['datasets']:
            ...     print(f"{dataset['name']}: {dataset['description']}")
        """
        # Import nemweb library directly - no FFI needed!
        from nemweb import nemweb_current
        
        datasets = []
        
        # AEMO datasets available via nemweb
        dataset_info = {
            'dispatch_scada': {
                'description': 'Dispatch SCADA data (generation unit output)',
                'update_frequency': '5min',
                'tables': ['DISPATCH_UNIT_SCADA']
            },
            'trading_is': {
                'description': 'Trading Interval Summary (30-min prices and demand)',
                'update_frequency': '30min',
                'tables': ['TRADING_PRICE', 'TRADING_REGIONSUM']
            },
            'rooftopPV_actual': {
                'description': 'Rooftop PV actual generation',
                'update_frequency': '30min',
                'tables': ['ROOFTOP_PV_ACTUAL']
            },
            'next_day_actual_gen': {
                'description': 'Next day actual generation forecast',
                'update_frequency': 'daily',
                'tables': ['NEXT_DAY_ACTUAL_GEN']
            },
            'next_day_dispatch': {
                'description': 'Next day dispatch forecast',
                'update_frequency': 'daily',
                'tables': ['NEXT_DAY_DISPATCH']
            },
            'dispatch_is': {
                'description': 'Dispatch interval summary',
                'update_frequency': '5min',
                'tables': ['DISPATCH_PRICE', 'DISPATCH_REGIONSUM']
            }
        }
        
        # Build response
        for name, info in dataset_info.items():
            if name in nemweb_current.DATASETS:
                datasets.append({
                    'name': name,
                    'description': info['description'],
                    'update_frequency': info['update_frequency'],
                    'tables': info['tables']
                })
        
        return {
            'datasets': datasets,
            'count': len(datasets)
        }
