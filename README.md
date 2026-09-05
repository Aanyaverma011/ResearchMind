# 🔬 ResearchMind — AI Research Agent

> An AI-powered multi-agent research system that searches the web, reads relevant sources, generates a structured research report, and evaluates the final output using an AI critic.

[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge)](https://research-mind-ai-agent.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/Aanyaverma011/ResearchMind)
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Multi--Agent-orange?style=for-the-badge)](https://www.langchain.com/)

---

## 🌐 Live Demo

🚀 **Try ResearchMind here:**

👉 **[Live ResearchMind App](https://research-mind-ai-agent.streamlit.app/)**

The application is deployed using **Streamlit Community Cloud** and can be accessed directly from a browser.

---

## 📌 Overview

**ResearchMind** is an AI-powered research assistant designed to automate the process of researching a topic and producing a concise, structured report.

Instead of relying on a single LLM call, ResearchMind uses a **multi-agent pipeline** where different components perform specialized tasks:

1. 🔎 **Search Agent** — Searches the web for recent and relevant information.
2. 📖 **Reader Agent** — Selects and reads a relevant source in depth.
3. ✍️ **Writer** — Combines the collected research into a structured report.
4. 🧐 **Critic** — Reviews the generated report for quality, clarity, completeness, and factual accuracy.

This creates a complete **Search → Read → Write → Critique** research workflow.

---

# 🧠 Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    │  Research Topic  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Search Agent   │
                    │                  │
                    │   Tavily Search  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Reader Agent   │
                    │                  │
                    │ Scrape Relevant  │
                    │     Source       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Writer      │
                    │                  │
                    │ Generate Report  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Critic      │
                    │                  │
                    │ Evaluate Report  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Final Research  │
                    │      Report      │
                    ___________________
```
✨ Key Features

🔎 AI-Powered Web Research

ResearchMind searches the web for relevant and recent information using Tavily.

🤖 Multi-Agent Architecture

Different agents are responsible for different stages of the research process instead of using a single AI prompt.

📖 Source Reading

The Reader Agent selects a relevant source and extracts useful information from it.

📝 Automated Report Generation

The Writer generates a professional research report containing:

Introduction
Key Findings
Conclusion
Sources
🧐 AI-Powered Criticism

The Critic evaluates the generated report based on:

Factual quality
Clarity
Completeness
Structure

It also provides a score out of 10 and improvement suggestions.

📚 Research History

Previous research topics and generated reports can be accessed through the application's history section.

🎨 Interactive Streamlit UI

The application provides a clean and interactive interface with:

Research topic input
Pipeline progress
Research history
Report display
Critic feedback
Source information
☁️ Cloud Deployment

ResearchMind is deployed using Streamlit Community Cloud, making the application accessible through a public URL.

🛠️ Tech Stack
Technology	 Purpose
Python	 Core programming language
LangChain	 AI agent and LLM orchestration
Groq	 Fast LLM inference
Tavily	 Web search
BeautifulSoup	 Web scraping
Requests	 HTTP requests
Streamlit	 Interactive web application
python-dotenv	 Environment variable management
Git & GitHub	 Version control and source management
Streamlit  Community Cloud	Application deployment


🔄 How It Works

Step 1 — Enter a Topic

The user enters a research topic in the ResearchMind interface.

Example:

Artificial Intelligence in Healthcare
Step 2 — Search Agent

The Search Agent uses Tavily to find relevant web sources.

It collects:

Source titles
URLs
Relevant snippets
Recent information
Step 3 — Reader Agent

The Reader Agent selects a relevant source from the search results and scrapes the webpage.

The extracted information is then used as deeper research material.

Step 4 — Writer

The Writer combines the search results and scraped content to generate a structured research report.

Step 5 — Critic

The Critic evaluates the generated report and provides:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

Verdict:
...
Step 6 — Final Result

The user receives a complete research report along with critic feedback and source information.

<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/0026d24e-54b1-407a-95e6-d5537bc043a7" />

<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/3caca141-15ad-43b4-b8b4-affb5151ffe2" />

<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/9818ddac-0764-4645-9267-da5aeab600ed" />


📂 Project Structure
ResearchMind/
│
├── app.py                  # Streamlit user interface
│
├── agents.py               # Search & Reader agents + Writer & Critic chains
│
├── tools.py                # Tavily search and web scraping tools
│
├── pipeline.py             # Main research pipeline
│
├── requirements.txt        # Python dependencies
│
├── .gitignore              # Ignored files and secrets
│
└── README.md               # Project documentation


⚙️ Installation & Setup

1. Clone the Repository
git clone YOUR_GITHUB_REPO_URL
cd ResearchMind
2. Create a Virtual Environment
python -m venv .venv

Activate it:

macOS / Linux
source .venv/bin/activate
Windows
.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure API Keys

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

⚠️ Never commit your .env file or API keys to GitHub.

5. Run the Application
streamlit run app.py

The application will open in your browser.

🔐 Environment Variables

ResearchMind requires the following API keys:

Variable	Purpose
GROQ_API_KEY	Provides LLM inference through Groq
TAVILY_API_KEY	Provides web search capabilities

For deployment, these keys are configured securely using Streamlit Secrets rather than being stored in the GitHub repository.

☁️ Deployment

ResearchMind is deployed on Streamlit Community Cloud.

The deployment workflow is:

GitHub Repository
        │
        ▼
Streamlit Community Cloud
        │
        ▼
Install requirements.txt
        │
        ▼
Configure Streamlit Secrets
        │
        ▼
Deploy Application
        │
        ▼
Public ResearchMind URL

The live application is available here:

👉 ResearchMind — Live Demo

🚀 Future Improvements

Some possible improvements for future versions include:

 Multiple-source research instead of a single source
 PDF and document research
 Citation generation
 Export reports as PDF
 More advanced source verification
 Research topic suggestions
 User authentication
 Database-backed research history
 More specialized research agents
 Improved report visualization
🎯 Learning Outcomes

Building ResearchMind helped explore practical concepts including:

Multi-agent AI systems
LangChain agent orchestration
LLM-powered workflows
Prompt engineering
Web search integration
Web scraping
AI-generated content evaluation
Streamlit application development
API integration
Environment variable management
Git & GitHub
Cloud deployment
👩‍💻 Author

Aanya Verma

B.Tech Computer Science & Engineering
IET Lucknow

Connect
💻 GitHub: https://github.com/Aanyaverma011
💼 LinkedIn: https://www.linkedin.com/in/aanya-verma-74a1872a3/

If you find ResearchMind useful or interesting, consider giving the repository a ⭐ on GitHub!




                    └──────────────────┘
