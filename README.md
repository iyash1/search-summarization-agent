
# 🤖 AI Search and Summarization Agent

> A search and summarization assistant powered by LangGraph, OpenAI, and Tavily Search 🌍📊

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Workflows](#workflows)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The **Search and Summarization Agent** is a sophisticated agentic AI application that helps users search the web and summarize topics. It leverages advanced language models and web search to provide comprehensive insights, concise summaries, sentiment analysis, and multilingual support.

## ✨ Features

- 📝 **Text Summarization** - Condense information into concise summaries
- 🌐 **Web Search Integration** - Real-time search for latest information and events
- 🇪🇸 **Multi-language Translation** - Translate summaries to Spanish (for now)
- 😊 **Sentiment Analysis** - Analyze content sentiment
- 🧠 **Agentic Workflow** - Advanced LangGraph-based agent architecture
- 🎨 **Colored CLI** - Beautiful terminal interface with emojis

## 📦 Prerequisites

Before you begin, ensure you have:

- 🐍 **Python 3.10+** installed
- 🔑 **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- 🔍 **Tavily API Key** ([Get one here](https://tavily.com))
- 📦 **Miniconda or Virtual Environment** for Python dependency isolation

## 📁 Project Structure

```
search-summarization-agent/
├── 📄 README.md                    # This file
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env                         # Environment variables (create this)
├── 🚀 app.py                       # Main application entry point
│
├── 📂 data/                        # Data models and constants
│   ├── __init__.py
│   ├── constants.py                # API endpoints and config values
│   └── models.py                   # TypedDict state definitions
│
├── 📂 nodes/                       # Individual processing nodes
│   ├── __init__.py
│   ├── summarize.py                # Text summarization logic
│   ├── translate.py                # Translation to Spanish
│   └── sentiment.py                # Sentiment analysis
│
├── 📂 workflows/                   # LangGraph workflow definitions
│   ├── __init__.py
│   ├── summarization.py            # Simple summarization workflow
│   ├── summary_and_translation.py  # Summary + translation workflow
│   └── summary_and_sentiment.py    # Summary + sentiment workflow
│
├── 📂 tools/                       # External tool integrations
│   ├── __init__.py
│   └── tavily_search.py            # Web search via TavilySearch
│
└── 📂 utils/                       # Helper utilities
    ├── __init__.py
    ├── helpers.py                  # Input validation and user prompts
    └── sample_prompts.py           # Test data for automated testing
```

## 🏗️ Folder Explanations

| Folder | Purpose |
|--------|---------|
| **data/** | Stores TypedDict models defining state structures and app constants |
| **nodes/** | Individual processing nodes that perform specific tasks (summarize, translate, sentiment) |
| **workflows/** | LangGraph StateGraph definitions that chain nodes together |
| **tools/** | External integrations like web search API wrappers |
| **utils/** | Helper functions for input validation, prompts, and sample data |

## 🚀 Installation

### Step 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/search-summarization-agent.git
cd search-summarization-agent
```

### Step 2️⃣ Create a Virtual Environment

**Using Miniconda (Recommended):**

```bash
# Install miniconda if not already installed
conda create -n search-agent python=3.10
conda activate search-agent
```

**Using Python venv:**

```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### Step 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output shows packages like `langchain`, `langgraph`, `langchain-openai`, etc. being installed. ✅

## 🔐 Configuration

### Step 1️⃣ Create .env File

Create a `.env` file in the project root:

```bash
touch .env
```

### Step 2️⃣ Add Your API Keys

Open `.env` and add:

```env
OPENAI_API_KEY=sk-proj-your-key-here
TAVILY_API_KEY=tvly-dev-your-key-here
DEBUG=False
AUTOMATED_TESTING=False
```

⚠️ **IMPORTANT**: Never commit `.env` to version control. Add it to `.gitignore`.

## 💻 Usage

### Running the Application

```bash
python app.py
```

You'll see a menu:

```
--------------------------------------
SELECT A WORKFLOW TO RUN:
--------------------------------------
1. Summarize only
2. Summarize and Translate to Spanish
3. Summarize and Analyze Sentiment
4. Search web for latest information
5. Exit
```

### Example Workflow

**Input:** "Tell me about electric vehicles"

**Workflow 1 (Summarize):**
```
=== Generated Summary ===
Electric vehicles use rechargeable batteries to power electric motors, 
offering zero emissions and improved efficiency with regenerative braking.
```

**Workflow 2 (Summarize + Translate):**
```
=== Generated Summary ===
[English summary here]

=== Translated Summary ===
[Spanish translation here]
```

## 🔄 Workflows

### Workflow 1: Summarize Only 📝

**File:** `workflows/summarization.py`

- Takes user input text
- Generates a concise one-sentence summary
- Displays result

### Workflow 2: Summarize & Translate 🌐

**File:** `workflows/summary_and_translation.py`

- Summarizes input text
- Translates summary to Spanish
- Returns both versions

### Workflow 3: Summarize & Sentiment 😊

**File:** `workflows/summary_and_sentiment.py`

- Summarizes input text
- Analyzes sentiment (positive/negative/neutral)
- Displays both results

### Workflow 4: Web Search 🔍

**File:** `tools/tavily_search.py`

- Searches the web using Tavily Search
- Returns latest information and insights
- Built with LangGraph agent architecture

## 🐛 Troubleshooting

### ❌ "API Key not found" Error

**Solution:** Verify `.env` file exists in project root and contains valid keys:

```bash
cat .env  # View .env contents
```

### ❌ "ModuleNotFoundError" on import

**Solution:** Ensure virtual environment is activated:

```bash
conda activate search-agent    # If using Miniconda
source venv/bin/activate       # If using venv
```

### ❌ LangGraph visualization fails

**Solution:** Install graphviz system package:

```bash
# macOS
brew install graphviz

# Ubuntu
sudo apt-get install graphviz

# Windows
# Download from https://graphviz.org/download/
```

### ❌ Rate limit errors from OpenAI

**Solution:** Wait a moment and retry. Upgrade API plan if needed.

## 📚 Key Technologies

- 🤖 **LangChain** - LLM framework
- 📊 **LangGraph** - Agentic workflow orchestration
- 🧠 **OpenAI GPT-4** - Language model
- 🔍 **Tavily Search** - Web search integration
- 🎨 **Colorama** - Terminal styling

## 📝 Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Yes |
| `TAVILY_API_KEY` | Your Tavily Search API key | ✅ Yes |
| `DEBUG` | Enable debug output (True/False) | ❌ No |
| `AUTOMATED_TESTING` | Use sample prompts (True/False) | ❌ No |

## 🎓 Learning Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Guide](https://platform.openai.com/docs)
- [Tavily Search Docs](https://docs.tavily.com)

## 🤝 Contributing

Contributions welcome! 🎉 Please open issues and pull requests.

## 📄 License

MIT License - see LICENSE file for details.

---

**Happy searching and summarizing! 🌍📊** Feel free to reach out with questions or suggestions! 💬

