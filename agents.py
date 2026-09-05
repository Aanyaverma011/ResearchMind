
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# MODEL
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=800
)


# ============================================================
# HELPER
# ============================================================

def clean_text(text: str, max_chars: int) -> str:
    """
    Keep the amount of context sent to Groq under control.
    """
    if not text:
        return ""

    text = str(text)

    if len(text) <= max_chars:
        return text

    return text[:max_chars] + "\n...[content truncated]"


# ============================================================
# 1. SEARCH AGENT
# ============================================================

def build_search_agent():

    return create_agent(
        model=llm,
        tools=[web_search],

        system_prompt="""
You are a web research search agent.

Your ONLY job is to search the web for the user's topic.

Use the web_search tool.

Find:
- recent information
- reliable sources
- useful URLs
- important facts

IMPORTANT:
- Call web_search only ONCE.
- Do not repeatedly search.
- Do not scrape URLs.
- Do not invent URLs.
- After the search, return a concise list of the best results.
"""
    )


# ============================================================
# 2. READER AGENT
# ============================================================

def build_reader_agent():

    return create_agent(
        model=llm,
        tools=[scrape_url],

        system_prompt="""
You are a research reader agent.

Your job is to read one relevant source from the search results.

IMPORTANT:
- Choose ONE URL.
- Call scrape_url only ONCE.
- Do not perform another web search.
- Do not call any other tool.
- Extract only the important factual information.
- Return a concise research summary.
"""
    )


# ============================================================
# 3. WRITER
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert research writer.

Write a clear, factual and professional research report.

Do not invent facts.
Use only the supplied research.
"""
    ),

    (
        "human",
        """
Write a research report about:

Topic:
{topic}

Research:
{research}

Use this structure:

# Introduction

# Key Findings

Explain at least 3 important findings.

# Conclusion

# Sources

Include the URLs that appear in the research.

Keep the report informative but concise.
"""
    )
])

writer_chain = writer_prompt | llm | StrOutputParser()


# ============================================================
# 4. CRITIC
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a research report critic.

Evaluate the report for:
- factual quality
- clarity
- completeness
- structure

Be concise.
"""
    ),

    (
        "human",
        """
Review this research report:

{report}

Return:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

Verdict:
...
"""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()

