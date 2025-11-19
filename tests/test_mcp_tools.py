"""
Tests for nemweb MCP tools

Run with: pytest tests/
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class MockMCP:
    """Mock MCP server for testing"""
    def __init__(self):
        self.tools = {}
    
    def tool(self):
        def decorator(func):
            self.tools[func.__name__] = func
            return func
        return decorator


def test_discover_tool():
    """Test nemweb_discover tool"""
    from nemweb_mcp.tools.discover import register_discover_tool
    
    mcp = MockMCP()
    register_discover_tool(mcp)
    
    result = mcp.tools['nemweb_discover']()
    
    assert 'datasets' in result
    assert 'count' in result
    assert result['count'] > 0
    assert len(result['datasets']) == result['count']
    
    # Check dataset structure
    for ds in result['datasets']:
        assert 'name' in ds
        assert 'description' in ds
        assert 'update_frequency' in ds
        assert 'tables' in ds
        assert isinstance(ds['tables'], list)


def test_status_tool_no_database():
    """Test nemweb_status when database doesn't exist"""
    from nemweb_mcp.tools.status import register_status_tool
    
    mcp = MockMCP()
    register_status_tool(mcp)
    
    # Use a non-existent database name
    result = mcp.tools['nemweb_status'](db_name='nonexistent_test.db')
    
    assert 'exists' in result
    assert result['exists'] is False
    assert 'message' in result
    assert 'database_path' in result


def test_query_tool_validation():
    """Test query tool SQL validation"""
    from nemweb_mcp.tools.query import register_query_tool
    
    mcp = MockMCP()
    register_query_tool(mcp)
    
    # Test that non-SELECT queries are rejected
    with pytest.raises(ValueError, match="Only SELECT queries are allowed"):
        mcp.tools['nemweb_query'](sql="DROP TABLE test", db_name='test.db')
    
    with pytest.raises(ValueError, match="Only SELECT queries are allowed"):
        mcp.tools['nemweb_query'](sql="INSERT INTO test VALUES (1)", db_name='test.db')


def test_download_tool_validation():
    """Test download tool dataset validation"""
    from nemweb_mcp.tools.download import register_download_tool
    
    mcp = MockMCP()
    register_download_tool(mcp)
    
    # Test invalid dataset name
    with pytest.raises(ValueError, match="Unknown dataset"):
        mcp.tools['nemweb_download'](
            dataset='invalid_dataset',
            start_date='20240101'
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
