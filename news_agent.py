import config
from pydantic_ai import Agent, ModelRequest, RunContext, ModelResponse, UserPromptPart, TextPart
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from scrapper_tool import full_page_content, filter_main_news
import logging


# Configure the LLM model with Ollama provider
model = OpenAIChatModel(
    model_name=config.local_llm_model,
    provider=OllamaProvider(base_url=config.local_llm_url, api_key=config.local_llm_api_key)
)


# Create the news agent with specific instructions
support_agent = Agent(
    model,
    instructions=config.news_agent_instruction,
)


@support_agent.tool_plain
async def get_main_news() -> str:
    """
    Returns current main (short list of) news with sources links in Markdown.
    
    This tool retrieves the main news content from the configured base URL. 
    It's designed to be used when users request general news updates.
    
    For Dzen.ru specifically, it filters out only the "main" section of the page
    using the filter_main_news function to extract just the relevant news content.
    
    Returns:
        str: Markdown formatted string containing main news with source links
        
    Example:
        >>> asyncio.run(get_main_news())
        "# News Headline\n\nNews summary text..."
    """
    logging.info(f"Tool get_main_news called")
    try:
        news_list = await full_page_content()
        if config.base_news_url == "https://dzen.ru/news":
            return filter_main_news(news_list)
        else:
            return news_list
    except Exception as e:
        return f"Failed to retrieve news with following error: {str(e)}"


# @support_agent.tool
# async def get_all_news(ctx: RunContext) -> str:
#     """Returns current all news with sources links in Markdown. Used only when user requires specific theme news."""
#     print(f"Tool get_all_news called")
#     print("#" * 20)
#     news_list = await full_page_content()
#     return news_list


@support_agent.tool_plain
async def get_full_page_content(page_link: str) -> str:
    """
    Returns full page content in Markdown.
    
    This tool retrieves the complete content of a specific web page URL.
    It's designed to be used when users want detailed information about 
    a particular news article or source.
    
    Args:
        page_link (str): The URL of the page to retrieve content from
        
    Returns:
        str: Markdown formatted string containing the full page content
        
    Example:
        >>> asyncio.run(get_full_page_content("https://example.com/news/article"))
        "# Article Title\n\nFull article content..."
    """
    logging.info(f"Tool get_full_page_content called with argument: {page_link[:50]}")
    try:
        page_content = await full_page_content(page_link)
        return page_content
    except Exception as e:
        return f"Failed to retrieve page content with following error: {str(e)}"


def convert_dialog_to_pydantic_ai_format(messages_base_list: list) -> list:
    """
    Convert a list of dialog messages to the format expected by pydantic-ai.
    
    This utility function transforms conversation messages from a standard 
    dictionary format (with 'role' and 'content' keys) into the format
    required by the pydantic-ai Agent for processing.
    
    Args:
        messages_base_list (list): List of message dictionaries with 'role' and 'content' keys
        
    Returns:
        list: List of ModelRequest/ModelResponse objects in pydantic-ai format
        
    Example:
        >>> convert_dialog_to_pydantic_ai_format([{"role": "user", "content": "Hello"}])
        [ModelRequest(parts=[UserPromptPart(content="Hello")])]
    """
    formatted_messages_list = []
    for msg_item in messages_base_list:
        if msg_item.get("role") == "user":
            formatted_message = ModelRequest(parts=[UserPromptPart(content=msg_item.get("content"))])
            formatted_messages_list.append(formatted_message)
        elif msg_item.get("role") == "assistant":
            formatted_message = ModelResponse(parts=[TextPart(content=msg_item.get("content"))])
            formatted_messages_list.append(formatted_message)
        else:
            continue

    return formatted_messages_list


async def chat_with_agent(messages_list: list, user_question_to_ai: str) -> str:
    """
    Process a user question through the news agent with conversation history.
    
    This is the main entry point for interacting with the news agent. It takes 
    the current conversation history and the new user question, processes them
    through the agent, and returns the AI's response.
    
    Args:
        messages_list (list): List of previous conversation messages (role/content pairs)
        user_question_to_ai (str): The new question from the user
        
    Returns:
        str: The AI's response to the user question
        
    Example:
        >>> asyncio.run(chat_with_agent([{"role": "user", "content": "What's the news?"}], "Latest updates"))
        "Here are the latest news updates..."
    """
    result = await support_agent.run(user_prompt=user_question_to_ai, message_history=convert_dialog_to_pydantic_ai_format(messages_list))
    return result.output
