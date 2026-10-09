import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY not found. Check your .env file."
    )

tavily = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """Search the web for relevant and recent research sources."""

    try:
        response = tavily.search(
            query=query,
            max_results=5,
            search_depth="basic"
        )

        results = response.get("results", [])

        if not results:
            return "No search results found."

        output = []

        for result in results:
            output.append(
                f"Title: {result.get('title', 'Unknown')}\n"
                f"URL: {result.get('url', '')}\n"
                f"Snippet: {result.get('content', '')[:500]}"
            )

        return "\n\n---\n\n".join(output)

    except Exception as exc:
        return f"Web search failed: {exc}"


@tool
def scrape_url(url: str) -> str:
    """Fetch a public webpage and extract its readable text."""

    try:
        if not url.startswith(("https://", "http://")):
            return "Invalid URL. Only HTTP and HTTPS URLs are supported."

        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup([
            "script", "style", "nav", "footer",
            "header", "aside", "noscript"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if not text:
            return "No readable text was found on this webpage."

        return text[:6000]

    except requests.RequestException as exc:
        return f"Could not retrieve webpage: {exc}"
    except Exception as exc:
        return f"Scraping failed: {exc}"