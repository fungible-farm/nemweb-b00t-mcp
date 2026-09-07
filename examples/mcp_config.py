"""Example: MCP Server Configuration"""

CONFIG = {
    "mcpServers": {
        "nemweb": {
            "command": "uv",
            "args": ["run", "python", "-m", "nemweb_mcp.server"],
            "env": {
                "NEMWEB_DATA_DIR": "${HOME}/.b00t/data"
            }
        }
    }
}

if __name__ == "__main__":
    import json
    print(json.dumps(CONFIG, indent=2))
