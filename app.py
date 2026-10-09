
import re
import html
import time
import streamlit as st
from pipeline import run_research_pipeline

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="ResearchMind | AI Research Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

if "sample_topic" not in st.session_state:
    st.session_state.sample_topic = "Choose an example..."

if "run_time" not in st.session_state:
    st.session_state.run_time = None


def apply_sample_topic():
    sample = st.session_state.get("sample_topic", "")
    if sample != "Choose an example...":
        st.session_state.topic_input = sample


# --------------------------------------------------
# THEME
# --------------------------------------------------
DARK = st.session_state.dark_mode

if DARK:
    BG = "#0D0F14"
    SIDEBAR = "#11141B"
    PANEL = "#151922"
    PANEL_HOVER = "#1B202B"
    TEXT = "#F1F3F9"
    MUTED = "#969FB2"
    BORDER = "#292F3C"
    ACCENT = "#A78BFA"
    ACCENT_SOFT = "#241D3C"
    INPUT_BG = "#11141B"
else:
    BG = "#F5F6FA"
    SIDEBAR = "#FFFFFF"
    PANEL = "#FFFFFF"
    PANEL_HOVER = "#F0EDFF"
    TEXT = "#202333"
    MUTED = "#697086"
    BORDER = "#E1E4ED"
    ACCENT = "#7652D6"
    ACCENT_SOFT = "#F0EBFF"
    INPUT_BG = "#FFFFFF"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {{
        color-scheme: {"dark" if DARK else "light"};
    }}

    .stApp {{
        background: {BG};
        color: {TEXT};
        font-family: 'DM Sans', sans-serif;
    }}

    [data-testid="stSidebar"] {{
        background: {SIDEBAR};
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stSidebar"] * {{
        color: {TEXT};
    }}

    .block-container {{
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: {TEXT} !important;
        letter-spacing: -0.5px;
    }}

    p, li, label, .stMarkdown {{
        color: {TEXT};
    }}

    [data-testid="stCaptionContainer"] p,
    .muted {{
        color: {MUTED} !important;
    }}

    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {{
        background: {INPUT_BG} !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
    }}

    [data-testid="stSelectbox"] > div > div {{
        background: {PANEL} !important;
        color: {TEXT} !important;
        border-color: {BORDER} !important;
        border-radius: 10px !important;
    }}

    .stButton > button,
    .stDownloadButton > button {{
        border-radius: 10px;
        border: 1px solid {BORDER};
        min-height: 42px;
        font-weight: 600;
        transition: all 0.2s ease;
    }}

    .stButton > button[kind="primary"] {{
        background: {ACCENT};
        color: white;
        border: 1px solid {ACCENT};
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        border-color: {ACCENT};
        transform: translateY(-1px);
    }}

    [data-testid="stMetric"] {{
        background: {PANEL};
        padding: 18px;
        border: 1px solid {BORDER};
        border-radius: 14px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {TEXT} !important;
    }}

    [data-testid="stTabs"] button {{
        color: {MUTED};
    }}

    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: {ACCENT} !important;
    }}

    hr {{
        border-color: {BORDER};
    }}

    .brand {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 25px;
        font-weight: 700;
        letter-spacing: -1px;
        margin-bottom: 2px;
    }}

    .brand span {{
        color: {ACCENT};
    }}

    .eyebrow {{
        font-family: 'DM Mono', monospace;
        color: {ACCENT};
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 2px;
    }}

    .hero {{
        padding: 34px 0 24px 0;
    }}

    .hero-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(34px, 5vw, 55px);
        font-weight: 700;
        line-height: 1.1;
        letter-spacing: -2px;
        color: {TEXT};
        margin: 12px 0;
    }}

    .hero-title .gradient {{
        color: {ACCENT};
    }}

    .hero-subtitle {{
        color: {MUTED};
        font-size: 15px;
        line-height: 1.8;
        max-width: 650px;
    }}

    .panel {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 14px;
    }}

    .panel-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 17px;
        color: {TEXT};
        margin-bottom: 6px;
    }}

    .panel-description {{
        color: {MUTED};
        font-size: 13px;
        line-height: 1.7;
    }}

    .stage {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 13px 14px;
        border: 1px solid {BORDER};
        background: {PANEL};
        border-radius: 12px;
        margin-bottom: 9px;
    }}

    .stage-icon {{
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: {ACCENT_SOFT};
        color: {ACCENT};
        font-size: 17px;
        flex-shrink: 0;
    }}

    .stage-name {{
        font-weight: 600;
        font-size: 13px;
        color: {TEXT};
    }}

    .stage-detail {{
        color: {MUTED};
        font-size: 11px;
        margin-top: 3px;
    }}

    .source-card {{
        border: 1px solid {BORDER};
        background: {PANEL};
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        overflow-wrap: anywhere;
    }}

    .source-card a {{
        color: {ACCENT};
        text-decoration: none;
        font-weight: 600;
    }}

    .source-url {{
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        color: {MUTED};
        margin-top: 7px;
    }}

    .footer-note {{
        color: {MUTED};
        font-size: 11px;
        text-align: center;
        padding-top: 28px;
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        f'<div class="brand">Research<span>Mind</span> ✦</div>',
        unsafe_allow_html=True,
    )
    st.caption("AI-powered research studio")
    st.divider()

    st.markdown("### Appearance")
    st.toggle(
        "Dark mode",
        key="dark_mode",
        help="Switch between dark and light themes.",
    )

    st.divider()
    st.markdown("### Your workspace")
    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-title">✦ Research Assistant</div>
            <div class="panel-description">
                Turn a research question into a structured report with
                web evidence and an AI critique.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Research pipeline")
    stages = [
        ("⌕", "Search Agent", "Find relevant web information"),
        ("↗", "Reader", "Extract useful page content"),
        ("✎", "Research Writer", "Create the research report"),
        ("✓", "Research Critic", "Review quality and evidence"),
    ]

    for icon, name, description in stages:
        st.markdown(
            f"""
            <div class="stage">
                <div class="stage-icon">{icon}</div>
                <div>
                    <div class="stage-name">{name}</div>
                    <div class="stage-detail">{description}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.caption("Built with Streamlit · LangChain · Gemini · Tavily")
    st.caption("AI-generated research should be independently verified.")

# --------------------------------------------------
# HERO
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">✦ Intelligent research workspace</div>
        <div class="hero-title">
            Ideas into <span class="gradient">insights.</span>
        </div>
        <div class="hero-subtitle">
            Explore a topic, gather web evidence, generate a structured
            report, and review its limitations — all in one workspace.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# RESEARCH INPUT
# --------------------------------------------------
left, right = st.columns([1.65, 1], gap="large")

with left:
    st.markdown("### Start your research")
    st.markdown(
        '<div class="muted">What would you like to investigate today?</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    examples = [
        "Choose an example...",
        "How is generative AI changing healthcare?",
        "Applications of deep learning in medical image analysis",
        "How AI agents and RAG systems work",
        "Renewable energy trends and challenges",
        "The impact of AI on the data analyst profession",
    ]

    st.selectbox(
        "Need inspiration? Choose an example",
        examples,
        key="sample_topic",
        on_change=apply_sample_topic,
    )

    with st.form("research_form"):
        topic = st.text_area(
            "Research topic",
            key="topic_input",
            placeholder=(
                "Example: Compare the benefits, limitations, and real-world "
                "applications of RAG versus fine-tuning LLMs..."
            ),
            height=125,
            help="Be specific to get a more focused research report.",
        )

        submitted = st.form_submit_button(
            "✦  Generate research report",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not topic.strip():
            st.warning("Please enter a research topic first.")
        else:
            st.session_state.research_result = None
            st.session_state.run_time = None

            start_time = time.perf_counter()

            with st.spinner(
                "Researching the topic, reading sources, writing and reviewing..."
            ):
                try:
                    result = run_research_pipeline(topic.strip())
                    st.session_state.research_result = result
                    st.session_state.run_time = round(
                        time.perf_counter() - start_time, 1
                    )
                    st.session_state.last_topic = topic.strip()
                except Exception as exc:
                    st.error(
                        "The research pipeline failed. Check the terminal "
                        "for the full traceback and verify your API keys."
                    )
                    st.code(str(exc))

with right:
    st.markdown("### What you'll get")
    benefits = [
        (
            "01",
            "Web research",
            "Relevant search results and source URLs.",
        ),
        (
            "02",
            "Readable evidence",
            "Useful text extracted from available webpages.",
        ),
        (
            "03",
            "Structured report",
            "Introduction, key findings, limitations and conclusion.",
        ),
        (
            "04",
            "Critical review",
            "An AI-generated assessment of report quality and support.",
        ),
    ]

    for number, title, description in benefits:
        st.markdown(
            f"""
            <div class="panel">
                <div class="eyebrow">{number}</div>
                <div class="panel-title">{title}</div>
                <div class="panel-description">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
result = st.session_state.research_result

if result:
    st.divider()

    st.markdown(
        """
        <div class="eyebrow">✦ Research output</div>
        <h2>Research desk</h2>
        """,
        unsafe_allow_html=True,
    )

    report = str(result.get("report", "No report was returned."))
    feedback = str(result.get("feedback", "No critic feedback was returned."))
    search_results = str(result.get("search_results", ""))
    scraped_content = str(result.get("scraped_content", ""))
    last_topic = st.session_state.get("last_topic", "Research topic")

    source_text = search_results + "\n" + scraped_content
    urls = re.findall(r'https?://[^\s<>"\]]+', source_text)
    urls = list(dict.fromkeys(url.rstrip(".,;:)") for url in urls))

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Sources identified", len(urls))
    metric2.metric(
        "Report length",
        f"{len(report.split()):,} words",
    )
    metric3.metric(
        "Processing time",
        f"{st.session_state.run_time or 0} sec",
    )

    st.markdown(f"#### {last_topic}")

    report_tab, critic_tab, sources_tab, evidence_tab = st.tabs(
        [
            "📄 Research report",
            "◈ Critic review",
            "↗ Sources",
            "⌕ Search & evidence",
        ]
    )

    with report_tab:
        st.markdown(report)
        st.download_button(
            "↓ Download report (.md)",
            data=report,
            file_name="research_report.md",
            mime="text/markdown",
            key="download_report",
        )

    with critic_tab:
        st.markdown(feedback)
        st.download_button(
            "↓ Download critic review (.txt)",
            data=feedback,
            file_name="critic_review.txt",
            mime="text/plain",
            key="download_critic",
        )

    with sources_tab:
        if urls:
            st.caption(
                "These URLs were extracted from the pipeline's returned text. "
                "Check that each source is relevant and supports the report."
            )
            for index, url in enumerate(urls, start=1):
                safe_url = html.escape(url, quote=True)
                st.markdown(
                    f"""
                    <div class="source-card">
                        <div><strong>Source {index}</strong></div>
                        <div style="margin-top:8px">
                            <a href="{safe_url}" target="_blank" rel="noopener noreferrer">
                                Open source ↗
                            </a>
                        </div>
                        <div class="source-url">{html.escape(url)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info(
                "No URLs were detected in the returned search text. "
                "Check the Search & evidence tab and your search tool output."
            )

    with evidence_tab:
        st.markdown("#### Search agent output")
        if search_results.strip():
            st.text(search_results)
        else:
            st.info("The pipeline returned no search text.")

        st.divider()
        st.markdown("#### Retrieved webpage content")
        if scraped_content.strip():
            st.text(scraped_content)
        else:
            st.info("No webpage text was returned by the scraper.")

    st.caption(
        "Note: the critic is another AI review, not a guarantee of factual accuracy. "
        "Verify important claims against the original sources."
    )

st.markdown(
    '<div class="footer-note">RESEARCHMIND · THINK DEEPER. VERIFY BETTER.</div>',
    unsafe_allow_html=True,
)
