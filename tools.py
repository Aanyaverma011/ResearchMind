
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


# ============================================================
# WEB SEARCH
# ============================================================

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information.
    Returns a small number of useful results with URLs.
    """

    try:

        results = tavily.search(
            query=query,
            max_results=3
        )

        output = []

        for r in results.get("results", []):

            title = r.get("title", "")
            url = r.get("url", "")
            content = r.get("content", "")

            # Keep snippets short
            content = content[:200]

            output.append(
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Snippet: {content}"
            )

        return "\n\n---\n\n".join(output)

    except Exception as e:

        return f"Search failed: {str(e)}"


# ============================================================
# SCRAPE URL
# ============================================================

@tool
def scrape_url(url: str) -> str:
    """
    Scrape one URL and return useful clean text.
    """

    try:

        response = requests.get(
            url,
            timeout=8,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # IMPORTANT:
        # Don't send huge scraped pages to Groq
        return text[:5000]

    except Exception as e:

        return f"Could not scrape URL: {str(e)}"

