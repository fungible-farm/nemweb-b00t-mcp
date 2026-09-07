"""
nemweb MCP Server - Python-native fastmcp implementation

This MCP server provides AI agents with access to AEMO energy data through
standardized MCP tools. Uses fastmcp for direct Python integration with the
existing nemweb library.

Example usage:
    # Start the MCP server
    python -m nemweb_mcp.server
    
    # Or via uv
    uv run python -m nemweb_mcp.server
"""

from fastmcp import FastMCP
import os
from pathlib import Path

# Initialize FastMCP server
mcp = FastMCP("nemweb", dependencies=["pandas", "requests"])

# Configure data directory
DATA_DIR = Path(os.getenv("NEMWEB_DATA_DIR", Path.home() / ".b00t" / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Import tools
from .tools.discover import register_discover_tool
from .tools.download import register_download_tool
from .tools.query import register_query_tool
from .tools.update import register_update_tool
from .tools.status import register_status_tool
from .tools.schema import register_schema_tool

# Register all tools
register_discover_tool(mcp)
register_download_tool(mcp)
register_query_tool(mcp)
register_update_tool(mcp)
register_status_tool(mcp)
register_schema_tool(mcp)


def main():
    """Main entry point for the MCP server"""
    import sys
    
    # Configure logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
