import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
import config

def filter_main_news(md_content: str) -> str:
    return md_content.split("# Главное\n")[1].split("\n##")[0]


async def full_page_content(page_link: str = config.base_news_url) -> str:
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