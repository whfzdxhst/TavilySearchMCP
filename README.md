# Tavily Search MCP

Tavily Search MCP is a Streamable HTTP MCP server that exposes Tavily web search
and page extraction as MCP tools.

## Tools

- `web_search`: Search the web from a query string.
- `web_fetch`: Extract readable text content from a web page URL.

## Requirements

- Python 3.11+
- A Tavily API key
- An MCP client that supports `streamable_http`

## Installation

Create and activate your preferred Python environment, then install the project:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

Create a local environment file:

```bash
cp .env.example .env
```

Fill in `.env`:

```env
TAVILY_API_KEY=tvly-your-api-key
MCP_SERVER_HOST=127.0.0.1
MCP_SERVER_PORT=21029
MCP_SERVER_PATH=/mcp
MCP_ALLOWED_HOSTS=127.0.0.1,127.0.0.1:21029,localhost,localhost:21029
MCP_ALLOWED_ORIGINS=*
```

For a server deployment, set `MCP_SERVER_HOST=0.0.0.0` and add the public
domain or host, with port, to `MCP_ALLOWED_HOSTS`.

## Run The Server

```bash
python -m tavily_search_mcp.server
```

Default local endpoint:

```text
http://127.0.0.1:21029/mcp
```

Health check:

```bash
curl http://127.0.0.1:21029/health
```

## Test Client

List tools:

```bash
python -m tavily_search_mcp.client --url http://127.0.0.1:21029/mcp list-tools
```

Search the web:

```bash
python -m tavily_search_mcp.client --url http://127.0.0.1:21029/mcp web-search "Tavily Python SDK" --max-results 2
```

Fetch a page:

```bash
python -m tavily_search_mcp.client --url http://127.0.0.1:21029/mcp web-fetch "https://docs.tavily.com/"
```

## MCP Client Configuration

Local example:

```json
{
  "mcpServers": {
    "tavily-search": {
      "type": "streamable_http",
      "url": "http://127.0.0.1:21029/mcp",
      "headers": {}
    }
  }
}
```

Remote example:

```json
{
  "mcpServers": {
    "tavily-search": {
      "type": "streamable_http",
      "url": "https://your-domain.example/mcp",
      "headers": {}
    }
  }
}
```

## Deploy To A Server

You can deploy with your own SSH key:

```powershell
.\scripts\deploy_remote.ps1 -HostName "your-server.example" -User "ubuntu" -IdentityFile "<path-to-private-key>"
```

The script uploads the current working tree, excluding `.git`, `.env`, `.conda`,
and other local-only files. On the server it installs dependencies and starts
the MCP server.

Before exposing the service publicly, configure the server `.env` with the
correct host, port, and allowed hosts:

```env
TAVILY_API_KEY=tvly-your-api-key
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=21029
MCP_SERVER_PATH=/mcp
MCP_ALLOWED_HOSTS=your-domain.example,your-domain.example:21029
MCP_ALLOWED_ORIGINS=*
```

## Security

- Never commit `.env` or real API keys.
- Never commit SSH keys, server IPs, private hostnames, or local key paths.
- Keep public deployments behind firewall, security group, proxy, or gateway
  rules appropriate for your environment.
- Rotate any key that was accidentally shared or committed.
