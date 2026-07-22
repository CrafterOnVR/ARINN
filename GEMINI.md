## Project Overview

This project is a Python-based autonomous research agent named ARINN. It is designed to perform time-boxed research on a given topic. The agent starts with an initial learning phase, then moves into a deep research phase driven by questions it generates. It can work with or without a Large Language Model (LLM) like OpenAI's GPT series. When an LLM is available, it's used for generating research questions and summarizing findings. Otherwise, it falls back to heuristic methods.

The agent is capable of:
-   Performing web searches using DuckDuckGo.
-   Fetching and parsing web page content.
-   Storing and deduplicating research findings in a local SQLite database.
-   Advanced capabilities include state-changing web actions, browser automation with Selenium, and git integration for versioning research progress.
-   A new desktop GUI built with PyQt6 provides a user-friendly interface for interacting with the agent.

## Building and Running

### Dependencies
The project's dependencies are listed in `requirements.txt`. Key libraries include:
-   `requests`, `beautifulsoup4`, `lxml`, `readability-lxml` for web scraping.
-   `duckduckgo_search` for web search.
-   `tenacity` for retrying failed operations.
-   `tqdm` for progress bars.
-   `openai` for interacting with OpenAI's APIs.
-   `PyQt6` for the desktop GUI.
-   `selenium`, `webdriver-manager` for browser automation.
-   `GitPython` for git integration.
-   `chromadb` for long-term memory.

### Setup and Execution
1.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run from the command line:**
    -   To start interactive research:
        ```bash
        python -m research_agent
        ```
    -   To research a specific topic:
        ```bash
        python -m research_agent --topic "your topic"
        ```
4.  **Run the Desktop GUI:**
    ```bash
    pip install PyQt6
    python run_desktop_gui.py
    ```

## Development Conventions

-   The project follows a modular structure, with different functionalities separated into different files (e.g., `db.py`, `search.py`, `fetch.py`, `llm.py`).
-   The agent's core logic is in `agent.py`, which defines the `ResearchAgent` class and its research phases.
-   The project uses both relative and absolute imports to support both package and direct execution.
-   Asynchronous operations are used for fetching web content and interacting with the LLM.
-   The agent can be configured via command-line arguments.
-   There is a strong emphasis on safety, with state-changing web actions being opt-in.
-   The project is version-controlled with git, and the agent can automatically commit snapshots of its progress.
