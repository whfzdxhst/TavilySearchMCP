from __future__ import annotations

from contextlib import asynccontextmanager
from functools import lru_cache
import warnings
from typing import Any, AsyncIterator, Literal

warnings.filterwarnings(
    "ignore",
    message="Field 'lifespan' has an incomplete definition.*",
    category=UserWarning,
)

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from tavily_search_mcp.config import get_settings
from tavily_search_mcp.tavily_service import SearchDepth, TavilySearchService, Topic


settings = get_settings()

mcp = FastMCP(
    name="tavily-search-mcp",
    stateless_http=True,
    json_response=False,
    transport_security=TransportSecuritySettings(
        allowed_hosts=settings.allowed_host_list,
        allowed_origins=settings.allowed_origin_list,
    ),
)


@lru_cache
def get_service() -> TavilySearchService:
    if not settings.tavily_api_key:
        raise RuntimeError("TAVILY_API_KEY is required to call Tavily-backed tools.")
    return TavilySearchService(api_key=settings.tavily_api_key)


@mcp.tool()
def web_search(
    query: str,
    max_results: int = 5,
    search_depth: SearchDepth = "basic",
    topic: Topic = "general",
    include_answer: bool = True,
    include_raw_content: bool = False,
    include_images: bool = False,
) -> dict[str, Any]:
    """Search the web using Tavily.

    Args:
        query: Search keywords or a natural-language question.
        max_results: Number of results to return, from 1 to 20.
        search_depth: Tavily search depth, either basic or advanced.
        topic: Search topic, one of general, news, or finance.
        include_answer: Include Tavily's generated answer when available.
        include_raw_content: Include raw page content in search results.
        include_images: Include related images when available.
    """

    return get_service().web_search(
        query=query,
        max_results=max_results,
        search_depth=search_depth,
        topic=topic,
        include_answer=include_answer,
        include_raw_content=include_raw_content,
        include_images=include_images,
    )


@mcp.tool()
def web_fetch(
    url: str,
    extract_depth: SearchDepth = "basic",
    include_images: bool = False,
    format: Literal["markdown", "text"] = "markdown",
) -> dict[str, Any]:
    """Fetch readable text content from a concrete web page URL.

    Args:
        url: The web page URL to extract.
        extract_depth: Tavily extraction depth, either basic or advanced.
        include_images: Include image URLs detected on the page.
        format: Returned content format, markdown or text.
    """

    normalized_format = "text" if format == "text" else "markdown"
    return get_service().web_fetch(
        url=url,
        extract_depth=extract_depth,
        include_images=include_images,
        format=normalized_format,
    )


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with mcp.session_manager.run():
        yield


def create_app() -> FastAPI:
    """Create the FastAPI host application for the MCP ASGI app."""

    app = FastAPI(
        title="Tavily Search MCP",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "name": "tavily-search-mcp"}

    app.mount("/", mcp.streamable_http_app())
    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(
        "tavily_search_mcp.server:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=False,
    )


if __name__ == "__main__":
    main()
