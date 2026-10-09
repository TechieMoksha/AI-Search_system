import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Check your .env file."
    )


# Shared Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY,
    timeout=60,
    max_retries=2
)


# Search agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a web research agent. Search for reliable, "
            "relevant sources about the user's topic. Use the "
            "web_search tool and summarize the findings with URLs. "
            "Never invent search results or sources."
        )
    )


# Writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a professional research writer.
Use the supplied research evidence.
Do not invent facts, statistics, or citations.
Clearly distinguish established facts from uncertainty."""
    ),
    (
        "human",
        """Write a structured research report on this topic:

Topic: {topic}

Research material:
{research}

Use these sections:
1. Introduction
2. Key Findings (at least 3 detailed findings)
3. Limitations or Research Gaps
4. Conclusion
5. Sources

Include source URLs from the supplied research.
If evidence is insufficient, state that clearly."""
    )
])

writer_chain = writer_prompt | llm | StrOutputParser()


# Critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a rigorous research critic.
Evaluate factual support, relevance, completeness,
clarity, and source quality. Do not reward invented citations."""
    ),
    (
        "human",
        """Critically review this research report:

{report}

Use this exact format:

Score: X/10

Strengths:
- Point 1
- Point 2

Areas to Improve:
- Point 1
- Point 2

Fact-checking Concerns:
- Mention unsupported claims, or state "None identified".

One-line Verdict:
..."""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()