# Fully Local News Agent

This is a simple fully local news agent, which using [crawl4ai](https://github.com/unclecode/crawl4ai) and [pydantic-ai](https://github.com/pydantic/pydantic-ai) for getting page content and summarizing retrieved news. No external APIs are used—only a local LLM.

## 🚀 Quick Start 

1. Install all requirements:
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

3. Turn on your Ollama server or LM Studio with correct server API and check is chosen mode is able to use tools.


4. Test agent work:
```bash
python usage_sample.py
```


## Agent capabilities:
1) Get news and summarize it.
2) Get source of news page content and give details about specific news.

### Personal test: 

I tested this agent with gpt-oss-20b with low reasoning effort and qwen/qwen3-4b-2507 (LM Studio) with 32k context, and it produced high-quality summaries for my target news source.






