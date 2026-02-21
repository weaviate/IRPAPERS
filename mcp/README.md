# IRPAPERS-MCP

An MCP server (built with FastMCP 3.0) that exposes a collection of 166 academic papers on Information Retrieval and Large Language Models as tools and resources via the Model Context Protocol.

## Tools

| Tool | Description |
|------|-------------|
| `ask` | Ask a natural language question answered by a Weaviate QueryAgent over 3,230 page-level multimodal embeddings |
| `collection_status` | Check document count and load status of the IRPAPERS collection |

## Resources

| URI | Description |
|-----|-------------|
| `irpapers://status` | Live status of the Weaviate collection |
| `irpapers://info` | Static metadata (paper count, embedding type, schema) |

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed and on your PATH (`brew install uv` on macOS)
- A Weaviate Cloud cluster with an API key

## Install with Claude Desktop

1. Open your Claude Desktop config file:

   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the following entry inside `"mcpServers"`:

   ```json
   {
     "mcpServers": {
       "irpapers": {
         "command": "uv", # Run `which uv` to see where particularly you have installed this
         "args": [
           "run",
           "--project", "/ABSOLUTE/PATH/TO/irpapers/mcp",
           "python", "server.py"
         ],
         "env": {
           "WEAVIATE_URL": "your-weaviate-cluster-url",
           "WEAVIATE_API_KEY": "your-weaviate-api-key"
         }
       }
     }
   }
   ```

   Replace `/ABSOLUTE/PATH/TO/irpapers/mcp` with the actual path to this project directory, and fill in your Weaviate credentials.

3. Restart Claude Desktop completely.

4. Look for the hammer icon in the input box — that confirms the server loaded successfully.

> **Note:** Claude Desktop runs servers in an isolated environment with no access to your shell profile or locally installed packages. The `env` block is required because environment variables from `.bashrc`/`.zshrc` are not inherited.

Note: You can now use this to import the MCP server to Claude Code with:

`claude mcp add-from-claude-desktop`

If you want to remove it run:

`claude mcp remove irpapers`

## Running Standalone

```bash
# STDIO transport (default)
uv run python server.py

# Via FastMCP CLI
uv run fastmcp run server.py:mcp

# HTTP transport (edit server.py to use mcp.run(transport="http", port=8000))
uv run python server.py
```
