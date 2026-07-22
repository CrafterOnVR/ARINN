# Research Agent

An autonomous, time-boxed research agent that:
- Prompts for a topic
- Spends an initial hour learning “what it is” via web search
- Generates questions and researches for 24 hours
- Deduplicates saved information per topic
- Prompts to continue for another 24 hours or summarize
- Can resume any learned topic for another 24 hours at any time
- Can manage its codebase with Git and perform safe self-edits (find/replace within the project)

What it does NOT do (by default):
- It does not perform any state-changing actions on the web. It only issues polite HTTP GET requests.

Enhanced capabilities (optional):
- State-changing web actions (POST, PUT, DELETE, form submission) when enabled with --enable-state-changing
- Browser automation with Selenium for JavaScript-heavy sites
- Interactive web research on specific URLs
- API requests with various HTTP methods

## 🚀 Advanced Automation Capabilities

The Enhanced Research Agent provides comprehensive automation across multiple domains:

### Advanced Browser Control
- **Full browser automation**: Chrome, Firefox with headless/visible modes
- **Complex interactions**: Click, type, scroll, drag-and-drop, form filling
- **Screenshot capabilities**: Full page, element-specific, with timestamps
- **JavaScript execution**: Run custom scripts and monitor results
- **Multi-tab management**: Open, close, switch between tabs
- **Network monitoring**: Capture and analyze HTTP requests

### Comprehensive GitHub Control
- **Repository management**: Create, clone, fork, delete repositories
- **Issue automation**: Create, update, close, assign issues
- **Pull request handling**: Create, merge, review PRs
- **File operations**: Create, update, delete files via API
- **Release management**: Create and manage releases
- **Search capabilities**: Find repositories, issues, code

### Advanced File System Control
- **File operations**: Create, read, write, copy, move, delete files
- **Directory management**: Create, delete, navigate directory structures
- **Content analysis**: Search, replace, analyze file contents
- **File watching**: Real-time monitoring of file system changes
- **Backup management**: Automatic backups with cleanup
- **Archive operations**: Create and extract ZIP/TAR archives

### Workflow Orchestration
- **Multi-step workflows**: Complex automation sequences
- **Parallel execution**: Run multiple operations simultaneously
- **Conditional logic**: Branch workflows based on conditions
- **Error handling**: Retry mechanisms and failure recovery
- **Progress tracking**: Monitor workflow execution in real-time

### Advanced Safety Controls
- **Permission system**: Role-based access control for all operations
- **Risk assessment**: Automatic risk evaluation for operations
- **Approval workflows**: Require approval for high-risk operations
- **Resource monitoring**: Track CPU, memory, disk usage
- **Audit logging**: Comprehensive security audit trails
- **Emergency controls**: Emergency stop and resume capabilities

## Requirements
- Python 3.10+
- Windows PowerShell (you are on Windows)

## Setup (PowerShell)
1) Create and activate a virtual environment
   - python -m venv .venv
   - .\\.venv\\Scripts\\Activate.ps1

2) Install dependencies
   - pip install -r research_agent\\requirements.txt

3) (Optional) Install enhanced web capabilities
   - pip install selenium webdriver-manager
   - Note: You'll also need to install Chrome or Firefox browser

4) (Optional) Configure OpenAI for better question generation and summaries
   - $env:OPENAI_API_KEY = "{{OPENAI_API_KEY}}"
   - # Optional: choose a model (default is gpt-4o-mini)
   - $env:OPENAI_MODEL = "gpt-4o-mini"

5) (Optional) Initialize Git in the project directory
   - python -m research_agent --git-init
   - python -m research_agent --git-branch main

Note: Do not paste secrets into scripts or commands you share. Keep keys in environment variables.

## 🖥️ Desktop GUI (New!)

The research agent now includes a professional desktop application powered by PyQt6!

### Launch the Desktop GUI
```bash
# Install PyQt6 first
pip install PyQt6

# Run the desktop application
python run_desktop_gui.py
```

The desktop GUI will open in a native Windows application window.

### Desktop GUI Features
- **Native Windows Application**: Professional desktop app with native Windows styling
- **Interactive Research**: Enter topics and start research with one click
- **Real-time Progress**: Watch research progress with visual progress bars
- **Comprehensive Results**: View organized results across multiple tabs
- **Configuration Panel**: Customize research settings with checkboxes and dropdowns
- **Tabbed Results**: Organized display (Overview, Questions, Patterns, Automation, Insights, Report)
- **Logo Integration**: Custom logo display in the application header
- **Menu System**: File and Help menus with About dialog
- **Status Updates**: Live status updates and progress indicators

### Desktop GUI Interface
- **Header**: Logo and title with professional styling
- **Research Configuration**: Topic input and advanced settings
- **Progress Tracking**: Visual progress bar and status messages
- **Results Tabs**: Six organized tabs for different research aspects
- **Control Buttons**: Start/Stop research with clear visual feedback

## Run (Command Line)
- Interactive prompt for a new topic:
  - python -m research_agent

- Provide a topic directly:
  - python -m research_agent --topic "quantum computing"

- Resume deep research on an existing topic for another 24h:
  - python -m research_agent --resume "quantum computing"

- Adjust time budgets (seconds):
  - python -m research_agent --topic "rust programming" --initial-seconds 1200 --deep-seconds 7200

- Disable LLM usage (use heuristic question generation and summary):
  - python -m research_agent --topic "blockchain" --no-llm

- Enable state-changing web actions (POST, PUT, DELETE, form submission):
  - python -m research_agent --topic "web APIs" --enable-state-changing

- Use browser automation for JavaScript-heavy sites:
  - python -m research_agent --topic "SPA frameworks" --enable-state-changing --selenium-driver chrome

- Research interactive URLs that require state-changing actions:
  - python -m research_agent --topic "online forms" --enable-state-changing --interactive-urls "https://example.com/form1" "https://example.com/form2"

- Run browser in visible mode (for debugging):
  - python -m research_agent --topic "web scraping" --enable-state-changing --no-headless

## 🚀 Advanced Usage Examples

### Enhanced Research Agent
```python
from research_agent.enhanced_agent import EnhancedResearchAgent

# Initialize with advanced capabilities
agent = EnhancedResearchAgent(enable_advanced=True)

# Comprehensive multi-modal research
research_config = {
    "enable_web_research": True,
    "enable_github_research": True,
    "enable_file_analysis": True,
    "web_urls": ["https://example.com", "https://research.org"]
}

results = agent.comprehensive_research("AI Safety", research_config)
```

### Browser Automation
```python
from research_agent.browser_controller import AdvancedBrowserController

browser = AdvancedBrowserController(driver_type="chrome", headless=True)
browser.start()

# Navigate and interact
browser.navigate_to("https://example.com")
browser.click_element("#submit-button")
browser.type_text("#search-box", "research query")
browser.take_screenshot("page_screenshot.png")
browser.close()
```

### GitHub Automation
```python
from research_agent.github_controller import AdvancedGitHubController

github = AdvancedGitHubController(token="your_token", username="your_username")

# Repository operations
repo = github.create_repository("research-project", "Research repository")
github.create_issue("owner", "repo", "Research Task", "Description")
github.create_pull_request("owner", "repo", "Feature PR", "feature-branch", "main")
```

### File System Operations
```python
from research_agent.file_controller import AdvancedFileController

file_controller = AdvancedFileController(base_path="./research", enable_watching=True)

# File operations
file_controller.create_file("notes.txt", "Research notes content")
results = file_controller.search_content("TODO|FIXME", directory="./code")
file_controller.create_archive("./data", "./backup.zip")
```

### Workflow Orchestration
```python
from research_agent.workflow_orchestrator import WorkflowOrchestrator, WorkflowStep

orchestrator = WorkflowOrchestrator(browser_controller, github_controller, file_controller)

# Create and execute workflow
steps = [
    WorkflowStep("navigate", "Navigate to site", "browser.navigate", {"url": "https://example.com"}),
    WorkflowStep("screenshot", "Take screenshot", "browser.screenshot", {"filename": "page.png"}),
    WorkflowStep("create_file", "Save data", "file.create_file", {"path": "data.txt", "content": "Research data"})
]

orchestrator.register_workflow("research_workflow", "Research Workflow", "Automated research", steps)
execution_id = orchestrator.start_execution("research_workflow", {"topic": "AI research"})
```

### Safety Controls
```python
from research_agent.safety_controller import AdvancedSafetyController, SecurityPolicy

safety = AdvancedSafetyController("safety_config.json")

# Create security policy
policy = SecurityPolicy(
    name="research_policy",
    allowed_actions={"browser.navigate", "file.create"},
    blocked_actions={"file.delete", "system.shutdown"},
    max_file_size=100*1024*1024,
    require_approval=True
)

safety.create_policy(policy)
safety.set_policy("research_policy")

# Request operation
has_permission, message, operation_id = safety.request_operation(
    user_id="researcher",
    action="browser.navigate",
    resource="https://example.com"
)
```

- Enable auto-commits during runs (snapshots at key phases):
  - python -m research_agent --topic "ai safety" --git-auto-commit --git-init

- Run a file (no prompt, runs anywhere by default):
  - python -m research_agent --run-file "C:\\Users\\dmdra\\research_agent\\scripts\\demo.py"
  - python -m research_agent --run-file "C:\\Users\\dmdra\\Downloads\\some.exe"

- Run a file as Administrator (Windows UAC prompt):
  - python -m research_agent --run-file "C:\\Windows\\System32\\notepad.exe" --run-as-admin
  - python -m research_agent --run-file "tool.ps1" --run-mode interpreter --run-as-admin

- Force interpreter mode and set timeout/cwd:
  - python -m research_agent --run-file "tool.ps1" --run-mode interpreter --run-timeout 90 --run-cwd .\\research_agent

- Create a directory (default scope is project root):
  - python -m research_agent --mkdir "C:\\temp\\research-output" --allow-any-path

- Create a file (from literal text):
  - python -m research_agent --create-file "notes\\plan.txt" --file-contents "Initial plan" --fs-root .\\research_agent

- Create a file by copying contents from a local file:
  - python -m research_agent --create-file "C:\\temp\\copied.txt" --file-contents-file "C:\\path\\to\\source.txt" --allow-any-path

- Export the project to a zip (auto-named in current directory):
  - python -m research_agent --export-project

- Export to a specific zip path and copy to filesystem directory:
  - python -m research_agent --export-project ".\\out\\research_agent.zip" --export-to "C:\\temp\\"

- List MTP devices/storages (Windows):
  - python -m research_agent --list-mtp

- Export and copy to an MTP path (example uses device/storage/folder):
  - python -m research_agent --export-project --export-mtp "My Phone/Internal Storage/Download"
  - Note: Install pywin32 (on Windows) if MTP copy fails.

- Automatic watch-and-copy to an allowlisted MTP path (opt-in):
  - python -m research_agent --watch-mtp "My Phone/Internal Storage/Download" --watch-interval 30
  - Add --watch-include-data if you want to include the data/ folder in the zip

## Data
The agent stores its SQLite database in:
- research_agent\\data\\research.db (inside the project directory)

It deduplicates saved information by hashing normalized text per topic and refuses to store duplicates. It also stores longer text snippets with deduplication to avoid re-learning identical content.

## Notes
- Web search: uses DuckDuckGo via the duckduckgo_search Python library.
- Fetching: politely requests pages and extracts readable text using readability-lxml when available (fallback to BeautifulSoup parsing).
- LLM: if OPENAI_API_KEY is set, the agent will ask the model to generate diverse questions and produce structured summaries. Otherwise it falls back to heuristics.
- Git: The agent can initialize a repo, switch/create branches, and auto-commit snapshots at key phases with --git-auto-commit.
- Self-edit & FS ops:
  - Safe by default: operations are restricted to the project directory unless you set --fs-root or --allow-any-path.
  - Find/replace within project (and optionally auto-commit):
    - python -m research_agent --self-edit-file "agent.py" --find "old text" --replace "new text" --git-auto-commit
  - Create directories and files:
    - python -m research_agent --mkdir "outputs" --fs-root .\\research_agent
    - python -m research_agent --create-file "outputs\\notes.txt" --file-contents "Hello" --fs-root .\\research_agent
- Running files:
  - You must pass --run-file; there is no confirmation prompt.
  - Paths are unrestricted by default (runs anywhere on disk). Use --run-cwd to set the working directory.
  - --run-as-admin elevates the run (Windows only); elevated processes run in a separate context and their output is not captured.
  - Interpreter mapping supports .py, .ps1, .bat/.cmd, .exe, .js, .sh; unknown types open with the OS default handler on Windows when in auto/open mode.
- Exporting:
  - Auto-transfer is opt-in via --watch-mtp and targets only the specified device path you provide.
  - One-shot zips and copies are available with --export-... commands.
  - On Windows, MTP copy requires pywin32 and an unlocked, connected device.
- Long runs: The deep research phase is intended to run for 24 hours. You can shorten for testing using --deep-seconds.

## Enhanced Web Capabilities & Safety

The research agent now supports state-changing web actions when explicitly enabled. These capabilities include:

### Features
- **Form submission**: Automatically fill and submit web forms
- **API requests**: Make POST, PUT, DELETE requests to web APIs
- **Browser automation**: Use Selenium WebDriver for JavaScript-heavy sites
- **Interactive research**: Research URLs that require user interaction

### Safety Controls
- **Rate limiting**: Maximum 30 requests per minute with 1-second delays
- **Domain filtering**: Block or allow specific domains
- **Opt-in only**: State-changing actions are disabled by default
- **Resource cleanup**: Automatic cleanup of browser instances

### Ethical Guidelines
- Always respect website terms of service
- Use appropriate delays between requests
- Don't overload servers with excessive requests
- Be mindful of data privacy and security
- Consider the impact on target websites

### Browser Requirements
- Chrome or Firefox browser must be installed
- WebDriver is automatically managed by webdriver-manager
- Headless mode is enabled by default for efficiency

