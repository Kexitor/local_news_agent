import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
import config

def filter_main_news(md_content: str) -> str:
    """
    Filter main news from markdown content by extracting content between "# Главное" and the next "##".
    
    This function is designed to extract only the main news section from a larger markdown document,
    typically used when scraping news websites that separate their main news from other content.
    
    Args:
        md_content (str): The full markdown content to filter
        
    Returns:
        str: Filtered markdown content containing only the main news section
    """
    return md_content.split("# Главное\n")[1].split("\n##")[0]


async def full_page_content(page_link: str = config.base_news_url) -> str:
    """
    Retrieve and crawl a web page content using AsyncWebCrawler.
    
    This function uses crawl4ai to fetch the content of a given URL and returns it as markdown.
    It's designed to work with local LLMs for processing news content.
    
    Args:
        page_link (str): The URL of the page to crawl. Defaults to config.base_news_url
        
    Returns:
        str: The markdown content of the crawled web page
        
    Example:
        >>> asyncio.run(full_page_content("https://example.com/news"))
        "# Example News\n\nThis is news content..."
    """
    browser_config = BrowserConfig(
        verbose=False,
    )
    run_config = CrawlerRunConfig(
        verbose=False,
        log_console=False,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=page_link,
            config=run_config,
        )
        # print(result.markdown)
        return result.markdown

if __name__ == "__main__":
    asyncio.run(full_page_content())
