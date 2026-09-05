import streamlit as st
import time
import re
import json
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# BACKEND IMPORTS
# ============================================================

from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)


# ============================================================
# HISTORY FILE
# ============================================================

HISTORY_FILE = Path(__file__).parent / "research_history.json"


def load_history():
    """Load previous research history from local JSON file."""

    try:
        if HISTORY_FILE.exists():

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

    except Exception:
        pass

    return []


def save_history(history):
    """Save research history locally."""

    try:

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                history,
                file,
                ensure_ascii=False,
                indent=2,
            )

    except Exception:
        pass


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 50% -15%,
                rgba(124, 58, 237, 0.20),
                transparent 42%
            ),
            radial-gradient(
                circle at 100% 70%,
                rgba(6, 182, 212, 0.08),
                transparent 35%
            ),
            #070912;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    html,
    body,
    [class*="css"] {
        font-family: "DM Sans", sans-serif;
    }


    /* ========================================================
       IMPORTANT:
       DO NOT HIDE THE STREAMLIT HEADER.
       
       The header contains the native sidebar button.
       ======================================================== */

    header {
        visibility: visible !important;
        background: transparent !important;
    }

   

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #090c16 0%,
                #080a13 100%
            );

        border-right:
            1px solid rgba(255,255,255,0.07);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-family: "Syne", sans-serif;
    }


 
    /* ========================================================
       MAIN BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius:
            13px !important;

        min-height:
            50px !important;

        border:
            1px solid
            rgba(255,255,255,0.10) !important;

        background:
            linear-gradient(
                135deg,
                #8b5cf6,
                #6d4aff 55%,
                #06b6d4
            ) !important;

        color:
            white !important;

        font-family:
            "Syne", sans-serif !important;

        font-weight:
            700 !important;

        box-shadow:
            0 10px 30px
            rgba(109,74,255,0.22) !important;

        transition:
            all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform:
            translateY(-2px);

        filter:
            brightness(1.08);

        box-shadow:
            0 14px 38px
            rgba(109,74,255,0.35) !important;
    }


    /* ========================================================
       TEXT INPUT
       ======================================================== */

    .stTextInput input {
        background:
            rgba(255,255,255,0.045) !important;

        color:
            #f5f5f7 !important;

        border:
            1px solid
            rgba(139,92,246,0.30) !important;

        border-radius:
            13px !important;

        min-height:
            52px !important;

        font-size:
            1rem !important;
    }

    .stTextInput input:focus {
        border-color:
            #8b5cf6 !important;

        box-shadow:
            0 0 0 3px
            rgba(139,92,246,0.10) !important;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero-badge {
        text-align:
            center;

        color:
            #a78bfa;

        font-size:
            0.72rem;

        font-weight:
            600;

        letter-spacing:
            0.18em;

        text-transform:
            uppercase;

        margin-bottom:
            1rem;
    }

    .hero-title {
        font-family:
            "Syne", sans-serif;

        font-size:
            clamp(3.5rem, 8vw, 6.8rem);

        font-weight:
            800;

        letter-spacing:
            -0.065em;

        line-height:
            0.95;

        text-align:
            center;

        margin-top:
            1rem;

        margin-bottom:
            1rem;

        color:
            #f7f7fa;
    }

    .hero-subtitle {
        text-align:
            center;

        max-width:
            700px;

        margin:
            0 auto;

        color:
            #9298aa;

        font-size:
            1.05rem;

        line-height:
            1.7;
    }


    /* ========================================================
       BORDERED CONTAINERS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color:
            rgba(255,255,255,0.08) !important;

        background:
            rgba(255,255,255,0.025);

        border-radius:
            18px;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {
        background:
            rgba(255,255,255,0.035);

        border:
            1px solid
            rgba(255,255,255,0.07);

        border-radius:
            15px;

        padding:
            15px;
    }


    /* ========================================================
       STATUS
       ======================================================== */

    [data-testid="stStatusWidget"] {
        border-radius:
            16px;
    }


    /* ========================================================
       REPORT
       ======================================================== */

    .report-heading {
        font-family:
            "Syne", sans-serif;

        color:
            #f3f4f6;
    }


    /* ========================================================
       SOURCE CARDS
       ======================================================== */

    .source-title {
        color:
            #e5e7eb;

        font-weight:
            600;
    }

    .source-url {
        color:
            #73798a;

        font-size:
            0.78rem;

        word-break:
            break-all;
    }


    /* ========================================================
       BOTTOM WEBSITE SECTION
       ======================================================== */

    .bottom-heading {
        font-family:
            "Syne", sans-serif;

        font-size:
            2rem;

        font-weight:
            800;

        color:
            #f3f4f6;
    }

    .bottom-description {
        color:
            #8f95a7;

        line-height:
            1.7;

        max-width:
            650px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-line {
        border-top:
            1px solid
            rgba(255,255,255,0.07);

        margin-top:
            50px;

        padding-top:
            28px;

        text-align:
            center;
    }

    .footer-brand {
        font-family:
            "Syne", sans-serif;

        font-size:
            1.1rem;

        font-weight:
            700;

        color:
            #e5e7eb;
    }

    .footer-small {
        color:
            #73798a;

        font-size:
            0.8rem;

        margin-top:
            7px;
    }

    .footer-tech {
        color:
            #8b5cf6;

        font-size:
            0.74rem;

        letter-spacing:
            0.08em;

        margin-top:
            11px;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left:
                1rem;

            padding-right:
                1rem;
        }

        .hero-title {
            font-size:
                3.5rem;
        }

        .hero-subtitle {
            font-size:
                0.9rem;
        }

    }

    /* ========================================================
   STREAMLIT HEADER + SIDEBAR TOGGLE
   ======================================================== */

/* Keep the Streamlit header visible */
header {
    visibility: visible !important;
    display: block !important;
    opacity: 1 !important;
    background: transparent !important;
    z-index: 999999 !important;
}

/* Do NOT hide the toolbar because the sidebar toggle
   can be inside Streamlit's header/toolbar */
[data-testid="stToolbar"] {
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 999999 !important;
}

/* Sidebar toggle - support multiple Streamlit versions */
[data-testid="stSidebarCollapsedControl"],
header [data-testid="stSidebarCollapsedControl"],
header button[aria-label="Open sidebar"],
header button[aria-label="Close sidebar"],
header button[title="Open sidebar"],
header button[title="Close sidebar"] {
    visibility: visible !important;
    display: flex !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}

/* Make the actual button VERY visible */
[data-testid="stSidebarCollapsedControl"] button,
header button[aria-label="Open sidebar"],
header button[aria-label="Close sidebar"],
header button[title="Open sidebar"],
header button[title="Close sidebar"] {
    width: 46px !important;
    height: 46px !important;

    min-width: 46px !important;
    min-height: 46px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    background: #ffffff !important;

    color: #111111 !important;

    border: 2px solid #8b5cf6 !important;

    border-radius: 12px !important;

    box-shadow:
        0 4px 18px rgba(0, 0, 0, 0.55),
        0 0 20px rgba(139, 92, 246, 0.35) !important;

    opacity: 1 !important;
    visibility: visible !important;

    pointer-events: auto !important;
}

/* Make the icon itself dark and obvious */
[data-testid="stSidebarCollapsedControl"] button svg,
header button[aria-label="Open sidebar"] svg,
header button[aria-label="Close sidebar"] svg,
header button[title="Open sidebar"] svg,
header button[title="Close sidebar"] svg {
    width: 24px !important;
    height: 24px !important;

    color: #111111 !important;

    fill: none !important;
    stroke: #111111 !important;

    opacity: 1 !important;
    visibility: visible !important;

    stroke-width: 2.5 !important;
}

/* Hover */
[data-testid="stSidebarCollapsedControl"] button:hover,
header button[aria-label="Open sidebar"]:hover,
header button[aria-label="Close sidebar"]:hover,
header button[title="Open sidebar"]:hover,
header button[title="Close sidebar"]:hover {
    background: #f3f0ff !important;
    border-color: #a78bfa !important;

    transform: scale(1.05) !important;

    box-shadow:
        0 6px 25px rgba(0, 0, 0, 0.6),
        0 0 28px rgba(139, 92, 246, 0.5) !important;
}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "results" not in st.session_state:
    st.session_state.results = {}

if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

if "pending_topic" not in st.session_state:
    st.session_state.pending_topic = None

if "research_time" not in st.session_state:
    st.session_state.research_time = 0.0

if "history" not in st.session_state:
    st.session_state.history = load_history()


# ============================================================
# APPLY PENDING TOPIC
# ============================================================

if st.session_state.pending_topic is not None:

    st.session_state.topic_input = (
        st.session_state.pending_topic
    )

    st.session_state.pending_topic = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def extract_score(text):
    """Extract critic score such as 8/10."""

    if not text:
        return None

    patterns = [
        r"score\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*/\s*10",
        r"(\d+(?:\.\d+)?)\s*/\s*10",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            return float(
                match.group(1)
            )

    return None


def extract_sources(text):
    """Extract source URLs from search output."""

    if not text:
        return []

    sources = []


    # --------------------------------------------------------
    # Title + URL format
    # --------------------------------------------------------

    pattern1 = re.compile(
        r"Title:\s*(.*?)\s*"
        r"URL:\s*(https?://[^\s)\]]+)",
        re.IGNORECASE | re.DOTALL,
    )

    for title, url in pattern1.findall(text):

        url = url.rstrip(
            ".,;"
        )

        sources.append(
            {
                "title": title.strip(),
                "url": url,
            }
        )


    # --------------------------------------------------------
    # Markdown links
    # --------------------------------------------------------

    pattern2 = re.compile(
        r"\[([^\]]+)\]"
        r"\((https?://[^)]+)\)"
    )

    for title, url in pattern2.findall(text):

        url = url.rstrip(
            ".,;"
        )

        if not any(
            source["url"] == url
            for source in sources
        ):

            sources.append(
                {
                    "title": title.strip(),
                    "url": url,
                }
            )


    # --------------------------------------------------------
    # Raw URLs
    # --------------------------------------------------------

    if not sources:

        urls = re.findall(
            r"https?://[^\s)\]]+",
            text,
        )

        for url in urls:

            url = url.rstrip(
                ".,;"
            )

            if not any(
                source["url"] == url
                for source in sources
            ):

                sources.append(
                    {
                        "title": url,
                        "url": url,
                    }
                )


    return sources


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🔬 ResearchMind"
    )

    st.caption(
        "Your AI research workspace"
    )

    st.divider()


    # ========================================================
    # HISTORY TITLE
    # ========================================================

    st.markdown(
        "### 🕘 Recent Research"
    )


    # ========================================================
    # HISTORY
    # ========================================================

    if not st.session_state.history:

        st.caption(
            "No research yet."
        )

        st.caption(
            "Your searches will appear here."
        )

    else:

        # Show newest first
        for index, item in enumerate(
            reversed(
                st.session_state.history
            )
        ):

            real_index = (
                len(
                    st.session_state.history
                )
                - 1
                - index
            )

            topic_name = str(
                item.get(
                    "topic",
                    "Untitled research",
                )
            )

            if len(topic_name) > 38:

                topic_name = (
                    topic_name[:38]
                    + "..."
                )


            # ------------------------------------------------
            # HISTORY BUTTON
            # ------------------------------------------------

            if st.button(
                "◷  " + topic_name,
                key=f"history_button_{real_index}",
                use_container_width=True,
            ):

                st.session_state.results = (
                    item.get(
                        "results",
                        {},
                    )
                )

                st.session_state.topic_input = (
                    item.get(
                        "topic",
                        "",
                    )
                )

                st.session_state.research_time = (
                    item.get(
                        "time",
                        0.0,
                    )
                )

                st.rerun()


    # ========================================================
    # CLEAR HISTORY
    # ========================================================

    st.divider()

    if st.button(
        "🗑  Clear History",
        key="clear_history_button",
        use_container_width=True,
    ):

        st.session_state.history = []

        save_history([])

        st.session_state.results = {}

        st.session_state.topic_input = ""

        st.rerun()


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero-badge">✦ MULTI-AGENT AI RESEARCH SYSTEM</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-title">ResearchMind</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-subtitle">
        Turn a question into a polished research report.
        Four specialized AI agents handle
        <b>search, reading, writing, and critical review.</b>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# ============================================================
# INPUT + PIPELINE
# ============================================================

input_col, pipeline_col = st.columns(
    [1.08, 0.92],
    gap="large",
)


# ============================================================
# INPUT
# ============================================================

with input_col:

    with st.container(border=True):

        st.markdown(
            "### Start a new research task"
        )

        st.caption(
            "What should ResearchMind investigate?"
        )

        topic = st.text_input(
            "Research topic",
            placeholder=(
                "e.g. How are AI agents changing software development?"
            ),
            key="topic_input",
            label_visibility="collapsed",
        )

        st.write("")

        run_button = st.button(
            "✦  Start Research",
            use_container_width=True,
        )

        st.write("")

        st.caption(
            "QUICK TOPICS"
        )

        quick1, quick2, quick3 = st.columns(3)


        # ----------------------------------------------------
        # QUICK TOPIC 1
        # ----------------------------------------------------

        with quick1:

            if st.button(
                "LLM Agents",
                use_container_width=True,
            ):

                st.session_state.pending_topic = (
                    "LLM agents in 2026"
                )

                st.rerun()


        # ----------------------------------------------------
        # QUICK TOPIC 2
        # ----------------------------------------------------

        with quick2:

            if st.button(
                "CRISPR",
                use_container_width=True,
            ):

                st.session_state.pending_topic = (
                    "Recent CRISPR gene editing breakthroughs"
                )

                st.rerun()


        # ----------------------------------------------------
        # QUICK TOPIC 3
        # ----------------------------------------------------

        with quick3:

            if st.button(
                "Fusion Energy",
                use_container_width=True,
            ):

                st.session_state.pending_topic = (
                    "Recent progress in fusion energy"
                )

                st.rerun()


# ============================================================
# PIPELINE PREVIEW
# ============================================================

with pipeline_col:

    st.markdown(
        "### Pipeline"
    )

    st.caption(
        "Four specialized agents working together"
    )


    pipeline_steps = [

        (
            "🔎",
            "Search Agent",
            "Find recent web information",
        ),

        (
            "📖",
            "Reader Agent",
            "Read the best source",
        ),

        (
            "✍️",
            "Writer Chain",
            "Create the report",
        ),

        (
            "🧐",
            "Critic Chain",
            "Review the report",
        ),

    ]


    for icon, name, description in pipeline_steps:

        with st.container(border=True):

            col_a, col_b = st.columns(
                [0.12, 0.88]
            )

            with col_a:

                st.write(icon)

            with col_b:

                st.markdown(
                    f"**{name}**"
                )

                st.caption(
                    description
                )


# ============================================================
# RUN PIPELINE
# ============================================================

if run_button:

    if not topic.strip():

        st.warning(
            "Please enter a research topic first."
        )

        st.stop()


    topic_value = topic.strip()

    start_time = time.perf_counter()

    results = {}


    # ========================================================
    # LIVE PIPELINE
    # ========================================================

    with st.status(
        "ResearchMind is working...",
        expanded=True,
    ) as status:


        # ====================================================
        # STEP 1 — SEARCH AGENT
        # ====================================================

        st.write(
            "🔎 **Search Agent** — searching for recent and reliable sources..."
        )

        try:

            search_agent = (
                build_search_agent()
            )

            search_result = (
                search_agent.invoke(
                    {
                        "messages": [
                            (
                                "user",
                                f"""
Find recent and reliable information about:

{topic_value}

Search only once and return the 3 most useful sources.
""",
                            )
                        ]
                    }
                )
            )

            search_content = (
                search_result[
                    "messages"
                ][-1].content
            )

            results["search"] = str(
                search_content
            )[:3500]

            st.write(
                "✓ Search Agent completed"
            )

        except Exception as e:

            st.error(
                f"Search Agent failed: {e}"
            )

            status.update(
                label="Research failed",
                state="error",
            )

            st.stop()


        # ====================================================
        # STEP 2 — READER AGENT
        # ====================================================

        st.write(
            "📖 **Reader Agent** — reading the most relevant source..."
        )

        try:

            reader_agent = (
                build_reader_agent()
            )

            reader_prompt = f"""
Topic:
{topic_value}

Search results:
{results["search"][:3000]}

Choose ONE relevant URL from the search results.

Scrape that URL once.

Return only the important factual information.
"""

            reader_result = (
                reader_agent.invoke(
                    {
                        "messages": [
                            (
                                "user",
                                reader_prompt,
                            )
                        ]
                    }
                )
            )

            reader_content = (
                reader_result[
                    "messages"
                ][-1].content
            )

            results["reader"] = str(
                reader_content
            )[:4500]

            st.write(
                "✓ Reader Agent completed"
            )

        except Exception as e:

            st.error(
                f"Reader Agent failed: {e}"
            )

            status.update(
                label="Research failed",
                state="error",
            )

            st.stop()


        # ====================================================
        # STEP 3 — WRITER
        # ====================================================

        st.write(
            "✍️ **Writer Chain** — creating your research report..."
        )

        try:

            research_combined = (
                "SEARCH RESULTS:\n"
                + results["search"][:2500]
                + "\n\n"
                + "SCRAPED RESEARCH:\n"
                + results["reader"][:4000]
            )

            writer_result = (
                writer_chain.invoke(
                    {
                        "topic": topic_value,
                        "research": research_combined,
                    }
                )
            )

            results["writer"] = str(
                writer_result
            )

            st.write(
                "✓ Writer Chain completed"
            )

        except Exception as e:

            st.error(
                f"Writer Chain failed: {e}"
            )

            status.update(
                label="Research failed",
                state="error",
            )

            st.stop()


        # ====================================================
        # STEP 4 — CRITIC
        # ====================================================

        st.write(
            "🧐 **Critic Chain** — checking report quality..."
        )

        try:

            critic_result = (
                critic_chain.invoke(
                    {
                        "report":
                            results["writer"][:5000]
                    }
                )
            )

            results["critic"] = str(
                critic_result
            )

            st.write(
                "✓ Critic Chain completed"
            )

        except Exception as e:

            st.error(
                f"Critic Chain failed: {e}"
            )

            status.update(
                label="Research failed",
                state="error",
            )

            st.stop()


        # ====================================================
        # COMPLETE
        # ====================================================

        elapsed = (
            time.perf_counter()
            - start_time
        )

        status.update(
            label="Research completed successfully",
            state="complete",
            expanded=False,
        )


    # ========================================================
    # SAVE CURRENT RESULT
    # ========================================================

    st.session_state.results = results

    st.session_state.research_time = elapsed




    # ========================================================
    # ADD TO HISTORY
    # ========================================================

    new_history_item = {
        "topic": topic_value,
        "results": results,
        "time": elapsed,
    }


    st.session_state.history.append(
        new_history_item
    )


    # Keep only the latest five
    st.session_state.history = (
        st.session_state.history[-5:]
    )


    # Save permanently
    save_history(
        st.session_state.history
    )


# ============================================================
# RESULTS
# ============================================================

results = st.session_state.results


if results:

    st.divider()


    # ========================================================
    # RESULT HEADER
    # ========================================================

    header_col, badge_col = st.columns(
        [0.78, 0.22]
    )


    with header_col:

        st.markdown(
            "## Research Report"
        )

        st.caption(
            "Research completed for: "
            + st.session_state.topic_input
        )


    with badge_col:

        st.success(
            "✓ Complete"
        )


    # ========================================================
    # METRICS
    # ========================================================

    sources = extract_sources(
        results.get(
            "search",
            "",
        )
    )

    score = extract_score(
        results.get(
            "critic",
            "",
        )
    )


    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )


    with metric1:

        st.metric(
            "Sources",
            len(sources),
        )


    with metric2:

        st.metric(
            "Agents",
            "4",
        )


    with metric3:

        st.metric(
            "Research Time",
            f"{st.session_state.research_time:.1f}s",
        )


    with metric4:

        if score is not None:

            st.metric(
                "Critic Score",
                f"{score:g}/10",
            )

        else:

            st.metric(
                "Critic Score",
                "—",
            )


    # ========================================================
    # REPORT
    # ========================================================

    st.markdown(
        "### 📄 Report"
    )


    if "writer" in results:

        with st.container(border=True):

            st.markdown(
                results["writer"]
            )


        st.write("")


        download_col1, download_col2, empty = (
            st.columns(
                [1, 1, 3]
            )
        )


        with download_col1:

            st.download_button(
                "↓  Download Markdown",
                data=results["writer"],
                file_name="researchmind_report.md",
                mime="text/markdown",
                use_container_width=True,
            )


        with download_col2:

            plain_text = re.sub(
                r"[#*_`]",
                "",
                results["writer"],
            )

            st.download_button(
                "↓  Download Text",
                data=plain_text,
                file_name="researchmind_report.txt",
                mime="text/plain",
                use_container_width=True,
            )


    # ========================================================
    # SOURCES
    # ========================================================

    st.markdown(
        "### 🔗 Sources"
    )


    if sources:

        for index, source in enumerate(
            sources,
            start=1,
        ):

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**{index:02d}  [{source['title']}]({source['url']})**"
                )

                st.caption(
                    source["url"]
                )

    else:

        st.caption(
            "No source URLs could be extracted from the search response."
        )


    # ========================================================
    # CRITIC REVIEW
    # ========================================================

    if "critic" in results:

        st.markdown(
            "### 🧐 Critical Review"
        )

        with st.container(border=True):

            st.markdown(
                results["critic"]
            )


# ============================================================
# BOTTOM WEBSITE SECTION
# ============================================================

st.write("")
st.write("")
st.divider()
st.write("")


st.markdown(
    '<div class="bottom-heading">Research, reimagined with AI.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="bottom-description">
        ResearchMind brings web search, source reading,
        report generation and critical evaluation together
        in one intelligent research workflow.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.write("")


# ============================================================
# BOTTOM IMAGE CARDS
# ============================================================

image1, image2, image3 = st.columns(
    3,
    gap="large",
)


# ============================================================
# IMAGE 1
# ============================================================

with image1:

    st.image(
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1000&q=85",
        use_container_width=True,
    )

    with st.container(border=True):

        st.markdown(
            "### 🔎 Intelligent Search"
        )

        st.caption(
            "Find recent and relevant information "
            "before building your research report."
        )


# ============================================================
# IMAGE 2
# ============================================================

with image2:

    st.image(
        "https://images.unsplash.com/photo-1555255707-c07966088b7b?auto=format&fit=crop&w=1000&q=85",
        use_container_width=True,
    )

    with st.container(border=True):

        st.markdown(
            "### 🧠 Multi-Agent Workflow"
        )

        st.caption(
            "Specialized agents work together across "
            "searching, reading, writing and reviewing."
        )


# ============================================================
# IMAGE 3
# ============================================================

with image3:

    st.image(
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1000&q=85",
        use_container_width=True,
    )

    with st.container(border=True):

        st.markdown(
            "### 🧐 Built-in Critic"
        )

        st.caption(
            "Every report is checked for clarity, "
            "structure, completeness and quality."
        )


# ============================================================
# FINAL WEBSITE SECTION
# ============================================================

st.write("")
st.write("")


with st.container(border=True):

    final_col1, final_col2 = st.columns(
        [1.4, 0.6],
        gap="large",
    )


    with final_col1:

        st.markdown(
            "### ✦ From question to research report."
        )

        st.caption(
            "Search → Read → Write → Critique"
        )


    with final_col2:

        st.metric(
            "AI Research Pipeline",
            "4 Agents",
        )

# ============================================================
# WEBSITE FOOTER
# ============================================================

st.write("")
st.write("")
st.divider()
st.write("")

st.markdown("## 🔬 ResearchMind")

st.caption(
    "An intelligent multi-agent research system designed to transform "
    "complex questions into structured, evidence-based research reports."
)

st.write("")

footer1, footer2, footer3, footer4 = st.columns(
    [1.4, 1, 1, 1],
    gap="large",
)

# ------------------------------------------------------------
# ABOUT
# ------------------------------------------------------------

with footer1:

    st.markdown("### About ResearchMind")

    st.caption(
        "ResearchMind automates the research workflow using "
        "specialized AI agents. Instead of manually searching, "
        "reading and organizing information, the system coordinates "
        "multiple agents to complete the process."
    )

    st.caption(
        "Built to make research faster, clearer and more organized."
    )


# ------------------------------------------------------------
# WORKFLOW
# ------------------------------------------------------------

with footer2:

    st.markdown("### ⚡ Workflow")

    st.caption("🔎 Search Agent")
    st.caption("📖 Reader Agent")
    st.caption("✍️ Writer Chain")
    st.caption("🧐 Critic Chain")

    st.caption(
        "Question → Search → Read → Write → Review"
    )


# ------------------------------------------------------------
# FEATURES
# ------------------------------------------------------------

with footer3:

    st.markdown("### ✦ Features")

    st.caption("• Real-time web research")
    st.caption("• Source-based information")
    st.caption("• Automated report generation")
    st.caption("• Built-in quality review")
    st.caption("• Research history")
    st.caption("• Markdown & text export")


# ------------------------------------------------------------
# TECHNOLOGY
# ------------------------------------------------------------

with footer4:

    st.markdown("### 🛠 Technology")

    st.caption("Streamlit")
    st.caption("LangChain")
    st.caption("Groq")
    st.caption("Tavily")
    st.caption("Python")
    st.caption("BeautifulSoup")


st.write("")
st.divider()
st.write("")

# ============================================================
# FOOTER BOTTOM
# ============================================================

bottom_left, bottom_right = st.columns(
    [1.5, 1],
    gap="large",
)

with bottom_left:

    st.markdown(
        "**🔬 ResearchMind**"
    )

    st.caption(
        "Search smarter. Read deeper. Write better. "
        "Review critically."
    )


with bottom_right:

    st.caption(
        "SEARCH  •  READ  •  WRITE  •  CRITIQUE"
    )

    st.caption(
        "Multi-Agent AI Research System"
    )


st.write("")

st.caption(
    "© 2026 ResearchMind · Built with Streamlit, LangChain, Groq & Tavily"
)