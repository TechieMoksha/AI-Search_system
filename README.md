
# ✦ ResearchMind — AI Multi-Agent Research System

An AI-powered research application that searches the web, extracts relevant information, 
generates structured research reports, and evaluates report quality using an AI critic.

## 🚀 Features

- **AI Search Agent:** Searches the web for relevant information using Tavily.
- **Web Content Extraction:** Retrieves and extracts useful text from webpages.
- **Research Writer:** Generates structured research reports using Google Gemini.
- **Research Critic:** Reviews reports for factual support, relevance, completeness, and clarity.
- **Interactive Dashboard:** Built with Streamlit, with dark and light theme support.
- **Report Export:** Download research reports in Markdown format and critic feedback as text files.

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini API
- Tavily Search API
- Requests
- BeautifulSoup
- python-dotenv
- 

## 📂 Project Structure

```text
AI-Search_system/
├── .venv/
├── .env
├── agents.py
├── app.py
├── main.py
├── pipeline.py
├── tools.py
├── test_gemini.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI-Search_system
```

### 2. Install dependencies

Install [uv](https://docs.astral.sh/uv/) if it is not already installed.

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root directory:

```env
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
```

Get your API keys from:

- [Tavily API](https://app.tavily.com/)
- [Google AI Studio](https://aistudio.google.com/apikey)


### 4. Run the application

```bash
uv run streamlit run app.py
```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/aa00fbe5-638a-41fb-bcbe-bdcb68ed40f0" />


## 🔄 How It Works

1. The user enters a research topic through the Streamlit dashboard.
2. The Search Agent uses Tavily to find relevant web information.
3. The application extracts useful content from selected webpages.
4. The Research Writer uses Gemini to generate a structured report.
5. The Research Critic evaluates the generated report and identifies potential weaknesses.
6. The dashboard displays the report, review, and available source URLs.

## 📄 Report Structure

Generated reports are organized into the following sections:

- Introduction
- Key Findings
- Limitations or Research Gaps
- Conclusion
- Sources

## 🔐 Environment Variables

| Variable | Purpose |
|---|---|
| `GOOGLE_API_KEY` | Accesses the Google Gemini API |
| `TAVILY_API_KEY` | Enables web search through Tavily |

## ⚠️ Limitations

- API requests are subject to provider quotas, rate limits, and service availability.
- Webpage extraction may fail on inaccessible or dynamically rendered websites.
- AI-generated findings and citations should be verified against the original sources.
- Research quality depends on the relevance and reliability of retrieved information.

## 🔮 Future Improvements

- Add exponential backoff and robust API error handling.
- Implement fallback models or providers.
- Improve source verification and citation tracking.
- Add research history and report management.
- Display real-time progress for individual pipeline stages.
- Add automated evaluation of report quality.

## 👩‍💻 Author

Developed as an AI and Generative AI project exploring multi-agent research workflows, web retrieval, automated report generation, and AI-based evaluation.
