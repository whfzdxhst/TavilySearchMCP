from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime configuration loaded from environment variables and .env."""

    tavily_api_key: str = ""
    server_host: str = "127.0.0.1"
    server_port: int = 21029
    server_path: str = "/mcp"
    allowed_hosts: str = Field(
        "127.0.0.1,127.0.0.1:21029,localhost,localhost:21029",
    )
    allowed_origins: str = "*"

    @property
    def allowed_host_list(self) -> list[str]:
        return _split_csv(self.allowed_hosts)

    @property
    def allowed_origin_list(self) -> list[str]:
        return _split_csv(self.allowed_origins)


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    load_dotenv(override=False)
    return Settings(
        tavily_api_key=os.getenv("TAVILY_API_KEY", ""),
        server_host=os.getenv("MCP_SERVER_HOST", "127.0.0.1"),
        server_port=int(os.getenv("MCP_SERVER_PORT", "21029")),
        server_path=os.getenv("MCP_SERVER_PATH", "/mcp"),
        allowed_hosts=os.getenv(
            "MCP_ALLOWED_HOSTS",
            "127.0.0.1,127.0.0.1:21029,localhost,localhost:21029",
        ),
        allowed_origins=os.getenv("MCP_ALLOWED_ORIGINS", "*"),
    )


def optional_settings() -> Settings | None:
    if not os.getenv("TAVILY_API_KEY"):
        load_dotenv(override=False)
    if not os.getenv("TAVILY_API_KEY"):
        return None
    return get_settings()
