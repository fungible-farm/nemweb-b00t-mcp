"""
Example: Basic nemweb MCP tool usage

This script demonstrates how to use the nemweb MCP tools directly.
"""

import sys
import os
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nemweb_mcp.tools.discover import register_discover_tool
from nemweb_mcp.tools.status import register_status_tool


class MockMCP:
    """Mock MCP server for testing tools directly"""
    def __init__(self):
        self.tools = {}
    
    def tool(self):
        """Decorator to register tools"""
        def decorator(func):
            self.tools[func.__name__] = func
            return func
        return decorator


def main():
    # Create mock MCP
    mcp = MockMCP()
    
    # Register tools
    register_discover_tool(mcp)
    register_status_tool(mcp)
    
    print("=" * 80)
    print("nemweb MCP Tools - Example Usage")
    print("=" * 80)
    
    # Example 1: Discover datasets
    print("\n1. Discover available datasets:")
    print("-" * 80)
    result = mcp.tools['nemweb_discover']()
    print(f"Found {result['count']} datasets:")
    for ds in result['datasets']:
        print(f"  - {ds['name']}: {ds['description']}")
        print(f"    Update frequency: {ds['update_frequency']}")
        print(f"    Tables: {', '.join(ds['tables'])}")
    
    # Example 2: Check status
    print("\n2. Check database status:")
    print("-" * 80)
    status = mcp.tools['nemweb_status']()
    if status.get('exists'):
        print(f"Database exists: {status['database_path']}")
    else:
        print(f"Database not found: {status['database_path']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
