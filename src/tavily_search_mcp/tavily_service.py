from __future__ import annotations

from typing import Any, Literal

from tavily import TavilyClient


SearchDepth = Literal["basic", "advanced"]
Topic = Literal["general", "news", "finance"]


class TavilySearchService:
    """Typed wrapper around the official Tavily Python SDK."""

    def __init__(self, api_key: str) -> None:
        self._client = TavilyClient(api_key=api_key)

    def web_search(
        self,
        query: str,
        *,
        max_results: int = 5,
        search_depth: SearchDepth = "basic",
        topic: Topic = "general",
        include_answer: bool = True,
        include_raw_content: bool = False,
        include_images: bool = False,
    ) -> dict[str, Any]:
        """Search the web with Tavily and return normalized result data."""

        clean_query = query.strip()
        if not clean_query:
            raise ValueError("query must not be empty")

        response = self._client.search(
            query=clean_query,
            max_results=max(1, min(max_results, 20)),
            search_depth=search_depth,
            topic=topic,
            include_answer=include_answer,
            include_raw_content=include_raw_content,
            include_images=include_images,
        )
        return self._normalize_search_response(response)

    def web_fetch(
        self,
        url: str,
        *,
        extract_depth: Literal["basic", "advanced"] = "basic",
        include_images: bool = False,
        format: Literal["markdown", "text"] = "markdown",
    ) -> dict[str, Any]:
        """Extract readable text content from a URL using Tavily Extract."""

        clean_url = url.strip()
        if not clean_url:
            raise ValueError("url must not be empty")

        response = self._client.extract(
            urls=[clean_url],
            extract_depth=extract_depth,
            include_images=include_images,
            format=format,
        )
        return self._normalize_extract_response(response)

    @staticmethod
    def _normalize_search_response(response: dict[str, Any]) -> dict[str, Any]:
        results = response.get("results") or []
        return {
            "query": response.get("query"),
            "answer": response.get("answer"),
            "images": response.get("images", []),
            "results": [
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content"),
                    "score": item.get("score"),
                    "published_date": item.get("published_date"),
                    "raw_content": item.get("raw_content"),
                }
                for item in results
            ],
            "response_time": response.get("response_time"),
        }

    @staticmethod
    def _normalize_extract_response(response: dict[str, Any]) -> dict[str, Any]:
        results = response.get("results") or []
        failed_results = response.get("failed_results") or []
        return {
            "results": [
                {
                    "url": item.get("url"),
                    "raw_content": item.get("raw_content"),
                    "images": item.get("images", []),
                }
                for item in results
            ],
            "failed_results": failed_results,
            "response_time": response.get("response_time"),
        }

