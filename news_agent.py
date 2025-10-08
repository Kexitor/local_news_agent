import config
from pydantic_ai import Agent, ModelRequest, RunContext, ModelResponse, UserPromptPart, TextPart
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from scrapper_tool import full_page_content, filter_main_news
import logging


model = OpenAIChatModel(
    model_name=config.local_llm_model,
    provider=OllamaProvider(base_url=config.local_llm_url)
)


support_agent = Agent(
    model,
    instructions=config.news_agent_instruction,

)

@support_agent.tool_plain
async def get_main_news() -> str:
    """Returns current main (short list of) news with sources links in Markdown. Used when user requires main news."""
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
    """Returns full page content in Markdown.

    Args:
        page_link: link to source page

    Returns:
        str: Markdown with page content
    """
    logging.info(f"Tool get_full_page_content called with argument: {page_link[:50]}")
    try:
        page_content = await full_page_content(page_link)
        return page_content
    except Exception as e:
        return f"Failed to retrieve page content with following error: {str(e)}"



def convert_dialog_to_pydantic_ai_format(messages_base_list: list) -> list:
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


async def chat_with_agent(messages_list: list, user_question_to_ai: str):
    result = await support_agent.run(user_prompt=user_question_to_ai, message_history=convert_dialog_to_pydantic_ai_format(messages_list))
    return result.output