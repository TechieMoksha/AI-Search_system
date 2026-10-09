import re
import time

from rich import print

from agents import (
    build_search_agent,
    writer_chain,
    critic_chain
)
from tools import scrape_url


def extract_text(content) -> str:
    """Convert an LLM response into readable text."""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict) and item.get("text"):
                parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)

        return "\n".join(parts)

    return str(content)


def extract_urls(text: str) -> list:
    """Extract unique HTTP/HTTPS URLs from search results."""

    urls = re.findall(r'https?://[^\s<>"\]]+', text)

    cleaned_urls = []

    for url in urls:
        url = url.rstrip(".,;:)")
        if url not in cleaned_urls:
            cleaned_urls.append(url)

    return cleaned_urls


def run_research_pipeline(topic: str) -> dict:
    """Run the complete AI research pipeline."""

    if not topic or not topic.strip():
        raise ValueError("Please provide a research topic.")

    state = {}
    topic = topic.strip()

    # STEP 1: Search
    print("\n[bold cyan]STEP 1 — SEARCH AGENT[/bold cyan]")

    start = time.perf_counter()

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Research this topic: {topic}. "
                    "Search the web and return relevant findings "
                    "with source titles, URLs, and factual snippets."
                )
            }
        ]
    })

    state["search_results"] = extract_text(
        search_result["messages"][-1].content
    )

    print(
        f"[green]Search completed in "
        f"{time.perf_counter() - start:.2f} seconds.[/green]"
    )

    print("\n[bold]Search findings:[/bold]")
    print(state["search_results"])

    # STEP 2: Scrape the most relevant returned URL
    print("\n[bold cyan]STEP 2 — READER[/bold cyan]")

    start = time.perf_counter()
    urls = extract_urls(state["search_results"])

    state["scraped_content"] = ""

    for url in urls[:3]:
        print(f"Reading source: {url}")

        result = scrape_url.invoke({"url": url})

        if isinstance(result, str) and not result.startswith(
            ("Could not retrieve webpage:", "Scraping failed:")
        ):
            if not result.startswith("Invalid URL"):
                state["scraped_content"] += (
                    f"\n\nSource URL: {url}\n{result}"
                )

        if len(state["scraped_content"]) >= 6000:
            break

    if not state["scraped_content"]:
        state["scraped_content"] = (
            "No webpage content could be retrieved. "
            "Use the available search snippets and disclose "
            "this limitation in the report."
        )

    state["scraped_content"] = state["scraped_content"][:12000]

    print(
        f"[green]Reading completed in "
        f"{time.perf_counter() - start:.2f} seconds.[/green]"
    )

    # STEP 3: Writer
    print("\n[bold cyan]STEP 3 — RESEARCH WRITER[/bold cyan]")

    start = time.perf_counter()

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print(
        f"[green]Report drafted in "
        f"{time.perf_counter() - start:.2f} seconds.[/green]"
    )

    print("\n[bold]FINAL RESEARCH REPORT[/bold]")
    print(state["report"])

    # STEP 4: Critic
    print("\n[bold cyan]STEP 4 — CRITIC[/bold cyan]")

    start = time.perf_counter()

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print(
        f"[green]Review completed in "
        f"{time.perf_counter() - start:.2f} seconds.[/green]"
    )

    print("\n[bold]CRITIC FEEDBACK[/bold]")
    print(state["feedback"])

    return state


if __name__ == "__main__":
    research_topic = input(
        "\nEnter a research topic: "
    ).strip()

    try:
        result = run_research_pipeline(research_topic)
        print("\n[bold green]Research pipeline completed.[/bold green]")

    except KeyboardInterrupt:
        print("\n[yellow]Research cancelled by user.[/yellow]")

    except Exception as exc:
        print(f"\n[bold red]Pipeline failed:[/bold red] {exc}")
        raise