"""Research Tools.

This module provides search and content processing utilities for the research agent,
using Tavily for URL discovery and fetching full webpage content.
"""

import httpx
from langchain_core.tools import InjectedToolArg, tool
from markdownify import markdownify
from tavily import TavilyClient
from typing_extensions import Annotated, Literal

tavily_client = TavilyClient()


def fetch_webpage_content(url: str, timeout: float = 10.0) -> str:
    """Fetch and convert webpage content to markdown.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Webpage content as markdown
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = httpx.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return markdownify(response.text)
    except Exception as e:
        return f"Error fetching content from {url}: {str(e)}"


@tool(parse_docstring=True)
def tavily_search(
    query: str,
    max_results: Annotated[int, InjectedToolArg] = 1,
    topic: Annotated[
        Literal["general", "news", "finance"], InjectedToolArg
    ] = "general",
) -> str:
    """Search the web for information on a given query.

    Uses Tavily to discover relevant URLs, then fetches and returns full webpage content as markdown.

    Args:
        query: Search query to execute
        max_results: Maximum number of results to return (default: 1)
        topic: Topic filter - 'general', 'news', or 'finance' (default: 'general')

    Returns:
        Formatted search results with full webpage content
    """
    # Use Tavily to discover URLs
    search_results = tavily_client.search(
        query,
        max_results=max_results,
        topic=topic,
    )

    # Fetch full content for each URL
    result_texts = []
    for result in search_results.get("results", []):
        url = result["url"]
        title = result["title"]

        # Fetch webpage content
        content = fetch_webpage_content(url)

        result_text = f"""## {title}
**URL:** {url}

{content}

---
"""
        result_texts.append(result_text)

    # Format final response
    response = f"""🔍 Found {len(result_texts)} result(s) for '{query}':

{chr(10).join(result_texts)}"""

    return response


@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """用于对研究进展和决策进行战略性反思的工具。

    在每次搜索后使用此工具，系统地分析搜索结果并规划下一步行动。
    这会在研究流程中设置一个有意识的暂停点，以便做出更高质量的决策。

    使用时机：
    - 收到搜索结果后：我找到了哪些关键信息？
    - 决定下一步行动前：现有信息是否足以给出全面的回答？
    - 评估研究缺口时：我还缺少哪些具体信息？
    - 结束研究前：现在是否可以给出完整的回答？

    反思内容应包括：
    1. 当前发现分析：我收集到了哪些具体信息？
    2. 信息缺口评估：还缺少哪些关键内容？
    3. 质量评估：是否有足够的证据或示例来支持高质量回答？
    4. 战略决策：应该继续搜索，还是直接给出回答？

    Args:
        reflection: 对研究进展、发现、信息缺口和下一步行动的详细反思

    Returns:
        表示反思已记录并可用于决策的确认信息
    """
    return f"Reflection recorded: {reflection}"
