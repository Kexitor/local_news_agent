# Fully Local News Agent

This is a simple fully local news agent that uses [crawl4ai](https://github.com/unclecode/crawl4ai) and [pydantic-ai](https://github.com/pydantic/pydantic-ai) for getting page content and summarizing retrieved news. No external APIs are used—only a local LLM.

## 🚀 Quick Start 

1. Install all requirements (I used python 3.11):
```bash
# Install the package
pip install -r requirements.txt

# Run post-installation setup for crawl4ai
crawl4ai-setup

# Verify crawl4ai installation
crawl4ai-doctor
```

2. Set in `config.py` all required paths and urls (you may use other openai-like APIs):
```python
local_llm_url = "http://localhost:5000/v1" # local OpenAI-compatible API path

local_llm_model = "openai/gpt-oss-20b" # local model used for agentic tasks

local_llm_api_key = "123" # this is a placeholder required by the OpenAI-compatible client

base_news_url = "https://dzen.ru/news" # page url, where news comes from
```

3. Turn on your Ollama server or LM Studio with correct server API and check if chosen model is able to use tools.


4. Test agent work:
```bash
python usage_sample.py
```


## 📋 Architecture

This agent follows a modular architecture:
- **Scrapper Tool**: Handles web scraping using crawl4ai
- **News Agent**: Main agent logic that uses pydantic-ai with OpenAI-compatible LLM 
- **Configuration**: Centralized configuration management
- **Usage Sample**: Example implementation showing how to interact with the agent

## 🧠 Agent Capabilities
1) Get news and summarize it.
2) Get source of news page content and give details about specific news.

## 🔧 Configuration Options

- `local_llm_url`: URL of your local OpenAI-compatible API (e.g., Ollama or LM Studio)
- `local_llm_model`: Name of the local model to use for agentic tasks  
- `local_llm_api_key`: API key placeholder required by OpenAI-compatible client
- `base_news_url`: Base URL from which news is scraped
- `logs_path`: Path where log files will be stored
- `news_agent_instruction`: Agent's instructions that define its behavior and response rules

## 🧪 Testing

I tested this agent with gpt-oss-20b with low reasoning effort and qwen/qwen3-4b-2507 (LM Studio) with 32k context, and it produced high-quality summaries for my target news source.

## 🔍 Troubleshooting

If you encounter issues:
1. Ensure your local LLM server is running
2. Verify that the model specified in `config.py` is available in your LLM server
3. Check that crawl4ai is properly installed and configured
4. Confirm that the base_news_url is accessible and returns valid content
