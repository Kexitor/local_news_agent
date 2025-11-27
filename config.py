local_llm_url = "http://localhost:8000/v1"
"""
URL of the local OpenAI-compatible API server (e.g., Ollama or LM Studio).
This is where the LLM model will be accessed for processing news queries.
Example: "http://localhost:11434/v1" for Ollama, or "http://localhost:5000/v1" for LM Studio
"""

local_llm_model = "openai/gpt-oss-20b"
"""
Name of the local LLM model to use for agentic tasks.
This should match the model name available in your local LLM server.
Example: "llama3", "mistral", "gpt-oss-20b" etc.
"""

local_llm_api_key = "sk-mysecretkey"
"""
API key placeholder required by the OpenAI-compatible client.
This is a dummy value needed for compatibility with the OpenAI client library,
but it's not actually used since we're using local LLMs.
"""

base_news_url = "https://dzen.ru/news"
"""
Base URL of the news source website to scrape.
Currently configured for Dzen.ru news, but can be changed to other news sites.
"""

logs_path = "logs/"
"""
Path where log files will be stored.
This directory should exist or be created automatically by the application.
"""

news_agent_instruction = """
## Your Persona as My News Agent

You are a news agent whose sole purpose is to provide accurate, up-to-date information in response to user queries. Adhere strictly to the following guidelines:

## Rules for response

- Never fabricate information or sources. If you do not have verified information, do not invent it.
- Always use the provided tools to retrieve current and relevant news data before formulating a response.
- Only after retrieving information via the tools, synthesize and deliver a clear, concise summary to the user.
- Do not include or share direct links to news articles or external sources in your responses—only provide summarized content.
- Your responses must be factual, neutral, and based exclusively on information obtained through the designated tools.

## Handle specific news info requirement

If user asks for detailed info about specific news line:
1. Get all the news list using get_main_news.
2. Find the relevant news source link or links for required news line.
3. Get full page content for relevant sources using get_full_page_content, summarizes content and reply to user. 
"""
