# Tavily Search MCP

Tavily Search MCP 是一个基于 Streamable HTTP 的 MCP 服务，用于把 Tavily 的联网搜索和网页内容提取能力封装成 MCP 工具。

## 功能

- `web_search`：根据查询关键字进行联网搜索。
- `web_fetch`：根据网页 URL 提取可读文本内容。

## 环境要求

- Python 3.11+
- Tavily API Key
- 支持 `streamable_http` 的 MCP 客户端

## 安装

先创建并启用你自己的 Python 虚拟环境，然后安装依赖和当前项目：

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

复制环境变量模板：

```bash
cp .env.example .env
```

在 `.env` 中填写配置：

```env
TAVILY_API_KEY=tvly-your-api-key
MCP_SERVER_HOST=127.0.0.1
MCP_SERVER_PORT=21029
MCP_SERVER_PATH=/mcp
MCP_ALLOWED_HOSTS=127.0.0.1,127.0.0.1:21029,localhost,localhost:21029
MCP_ALLOWED_ORIGINS=*
```

如果部署到服务器，请将 `MCP_SERVER_HOST` 设置为 `0.0.0.0`，并把你的公网域名或访问主机名加入 `MCP_ALLOWED_HOSTS`。

## 启动服务

```bash
python -m tavily_search_mcp.server
```

默认本地 MCP 地址：

```text
http://127.0.0.1:21029/mcp
```

健康检查：

```bash
curl http://127.0.0.1:21029/health
```

## 测试客户端

列出 MCP 工具：

```bash
python -m tavily_search_mcp.client --url http://127.0.0.1:21029/mcp list-tools
```

调用联网搜索：

```bash
python -m tavily_search_mcp.client --url http://127.0.0.1:21029/mcp web-search "Tavily Python SDK" --max-results 2
```

调用网页内容提取：

```bash
python -m tavily_search_mcp.client --url http://127.0.0.1:21029/mcp web-fetch "https://docs.tavily.com/"
```

## MCP 客户端配置

本地服务示例：

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

远程服务示例：

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

## 部署到服务器

可以使用仓库中的部署脚本，通过你自己的 SSH key 上传并启动服务：

```powershell
.\scripts\deploy_remote.ps1 -HostName "your-server.example" -User "ubuntu" -IdentityFile "<path-to-private-key>"
```

