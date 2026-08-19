from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def list_tools(server_url: str, headers: dict[str, str] | None = None) -> None:
    async with streamablehttp_client(server_url, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(json.dumps(tools.model_dump(), ensure_ascii=False, indent=2))


async def call_tool(
    server_url: str,
    tool_name: str,
    arguments: dict[str, Any],
    headers: dict[str, str] | None = None,
) -> None:
    async with streamablehttp_client(server_url, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


def parse_headers(values: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for value in values:
        if ":" not in value:
            raise ValueError(f"Invalid header {value!r}; expected 'Name: value'.")
        name, header_value = value.split(":", 1)
        headers[name.strip()] = header_value.strip()
    return headers


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Test a Streamable HTTP Tavily MCP server.")
    parser.add_argument("--url", default="http://127.0.0.1:21029/mcp", help="MCP endpoint URL.")
    parser.add_argument("--header", action="append", default=[], help="Optional request header.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-tools")

    search_parser = subparsers.add_parser("web-search")
    search_parser.add_argument("query")
    search_parser.add_argument("--max-results", type=int, default=3)

    fetch_parser = subparsers.add_parser("web-fetch")
    fetch_parser.add_argument("page_url")

    args = parser.parse_args()
    headers = parse_headers(args.header)

    if args.command == "list-tools":
        asyncio.run(list_tools(args.url, headers=headers))
    elif args.command == "web-search":
        asyncio.run(
            call_tool(
                args.url,
                "web_search",
                {"query": args.query, "max_results": args.max_results},
                headers=headers,
            )
        )
    elif args.command == "web-fetch":
        asyncio.run(call_tool(args.url, "web_fetch", {"url": args.page_url}, headers=headers))


if __name__ == "__main__":
    main()
