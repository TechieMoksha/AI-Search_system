import html
import time

import streamlit as st

from pipeline import run_research_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearchMind | AI Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800'
      '&family=DM+Mono:wght@400;500'
      '&family=DM+Sans:wght@300;400;500;600&display=swap'
    );

    .stApp {
        background:
            radial-gradient(
                ellipse at 15% 0%,
                rgba(255,140,50,0.12),
                transparent 42%
            ),
            #0a0a0f;
        color: #e8e4dc;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    h1, h2, h3 {
        font-family: 'Syne', sans-serif !important;
        color: #f0ebe0 !important;
    }

    .hero {
        text-align: center;
        padding: 3rem 0 2rem;
    }

    .eyebrow {
        color: #ff8c32;
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
    }

    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: clamp(2.7rem, 6vw, 4.8rem);
        font-weight: 800;
        letter-spacing: -0.045em;
        line-height: 1.1;
        color: #f0ebe0;
        margin: 0.8rem 0;
    }

    .hero-title span {
        color: #ff8c32;
    }

    .hero-subtitle {
        color: #a09890;
        max-width: 650px;
        margin: 0 auto;
        font-size: 1rem;
        line-height: 1.8;
    }

    .divider {
        height: 1px;
        margin: 1.5rem 0 2rem;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255,140,50,0.4),
            transparent
        );
    }

    .section-label {
        color: #ff8c32;
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .panel {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,140,50,0.17);
        border-radius: 14px;
        padding: 1.35rem;
        margin-bottom: 1rem;
    }

    .pipeline-step {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin: 0.65rem 0;
    }

    .pipeline-step.active {
        border-color: #ff8c32;
        background: rgba(255,140,50,0.07);
    }

    .pipeline-step.done {
        border-color: rgba(80,200,120,0.45);
    }

    .step-title {
        color: #f0ebe0;
        font-weight: 600;
        font-size: 0.92rem;
    }

    .step-desc {
        color: #8f8982;
        font-size: 0.8rem;
        margin-top: 0.35rem;
    }

    .step-status {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.08em;
        color: #a09890;
        margin-top: 0.45rem;
    }

    .step-status.active {
        color: #ff8c32;
    }

    .step-status.done {
        color: #50c878;
    }

    .stTextInput input {
        background: rgba(255,255,255,0.045) !important;
        color: #f0ebe0 !important;
        border-color: rgba(255,140,50,0.3) !important;
        border-radius: 9px !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(
            135deg, #ff9a42, #ff681f
        ) !important;
        color: #14100d !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
        min-height: 2.8rem;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        box-shadow: 0 5px 22px rgba(255,140,50,0.2);
    }

    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
    }

    .footer {
        text-align: center;
        color: #605850;
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        margin-top: 3rem;
        letter-spacing: 0.08em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "active_step" not in st.session_state:
    st.session_state.active_step = -1

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Multi-Agent AI Research System</div>
        <div class="hero-title">Research<span>Mind</span></div>
        <div class="hero-subtitle">
            From web discovery to a structured research report.
            Search, extract, write and critique your topic
            using a Gemini-powered research pipeline.
        </div>
    </div>
    <div class="divider"></div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INPUT AND PIPELINE
# ============================================================

col_input, col_pipeline = st.columns(
    [1.15, 0.85],
    gap="large",
)

with col_input:
    st.markdown(
        '<div class="section-label">01 / Research configuration</div>',
        unsafe_allow_html=True,
    )

    with st.form("research_form"):
        topic = st.text_input(
            "RESEARCH TOPIC",
            placeholder="e.g. The impact of AI agents on healthcare",
            help="Enter a topic you want to investigate.",
        )

        submitted = st.form_submit_button(
            "⚡ Run Research Pipeline",
            use_container_width=True,
        )

    st.markdown(
        '<div class="panel"><div class="section-label">'
        'TRY A RESEARCH TOPIC</div></div>',
        unsafe_allow_html=True,
    )

    examples = [
        "Generative AI in healthcare",
        "Latest developments in quantum computing",
        "AI agents in data science",
    ]

    for example in examples:
        if st.button(
            example,
            key=f"example_{example}",
            use_container_width=True,
        ):
            st.session_state.selected_topic = example
            st.rerun()

    if "selected_topic" in st.session_state:
        if not topic:
            st.caption(
                f"Selected example: {st.session_state.selected_topic}"
            )
            st.info(
                "Copy the example into the research topic field "
                "and click Run Research Pipeline."
            )


with col_pipeline:
    st.markdown(
        '<div class="section-label">02 / Pipeline status</div>',
        unsafe_allow_html=True,
    )

    steps = [
        (
            "01",
            "Search Agent",
            "Finds relevant web sources using Tavily.",
        ),
        (
            "02",
            "Reader",
            "Extracts text from relevant webpages.",
        ),
        (
            "03",
            "Research Writer",
            "Creates a structured research report.",
        ),
        (
            "04",
            "Research Critic",
            "Reviews the report and provides feedback.",
        ),
    ]

    for index, (number, title, description) in enumerate(steps):
        if st.session_state.active_step == index:
            status = "RUNNING"
            card_class = "active"
            status_class = "active"
        elif (
            st.session_state.research_result is not None
            and st.session_state.active_step == 4
        ):
            status = "COMPLETED"
            card_class = "done"
            status_class = "done"
        else:
            status = "WAITING"
            card_class = ""
            status_class = ""

        st.markdown(
            f"""
            <div class="pipeline-step {card_class}">
                <div class="step-title">
                    {number} &nbsp; {title}
                </div>
                <div class="step-desc">{description}</div>
                <div class="step-status {status_class}">
                    {status}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# RUN PIPELINE
# ============================================================

if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        st.session_state.research_result = None
        st.session_state.active_step = 0
        st.session_state.last_topic = topic.strip()

        progress = st.progress(0)
        status_message = st.empty()

        try:
            with st.spinner(
                "Research is running. This may take a little while..."
            ):
                status_message.info(
                    "Searching the web and collecting research..."
                )

                result = run_research_pipeline(topic.strip())

                progress.progress(100)
                status_message.success("Research pipeline completed.")

                st.session_state.research_result = result
                st.session_state.active_step = 4

        except Exception as exc:
            st.session_state.active_step = -1
            st.error(
                f"Research failed: {exc}\n\n"
                "Check your API keys, model availability, "
                "network connection and terminal logs."
            )

        finally:
            progress.empty()

        st.rerun()


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.research_result

if result:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">03 / Research output</div>',
        unsafe_allow_html=True,
    )

    st.subheader(st.session_state.last_topic)

    search_results = result.get("search_results", "")
    scraped_content = result.get("scraped_content", "")
    report = result.get("report", "")
    feedback = result.get("feedback", "")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("Pipeline", "Completed")

    with metric2:
        st.metric(
            "Search output",
            f"{len(search_results):,} chars",
        )

    with metric3:
        st.metric(
            "Report length",
            f"{len(report):,} chars",
        )

    tab_report, tab_critic, tab_sources = st.tabs(
        [
            "📝 Research Report",
            "🧐 Critic Review",
            "🔎 Research Sources",
        ]
    )

    with tab_report:
        st.markdown(report or "No report was generated.")

        if report:
            safe_topic = "".join(
                c if c.isalnum() else "_"
                for c in st.session_state.last_topic
            )[:60]

            st.download_button(
                "⬇ Download report (.md)",
                data=report,
                file_name=f"research_report_{safe_topic}.md",
                mime="text/markdown",
                use_container_width=True,
            )

    with tab_critic:
        st.markdown(feedback or "No critic feedback was generated.")

    with tab_sources:
        with st.expander("Search results", expanded=True):
            st.text(search_results or "No search results available.")

        with st.expander("Scraped webpage content"):
            st.text(
                scraped_content or "No scraped content available."
            )

    st.caption(
        "Research reports may contain errors. Verify important claims "
        "against the original sources."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        RESEARCHMIND · GEMINI + LANGCHAIN + TAVILY + STREAMLIT
    </div>
    """,
    unsafe_allow_html=True,
)