from logging.handlers import TimedRotatingFileHandler
import sys
import logging
from news_agent import chat_with_agent
import asyncio
import os
import config

os.makedirs(config.logs_path, exist_ok=True)
handler = TimedRotatingFileHandler(config.logs_path + "logs.txt", when="midnight", backupCount=2)
handler.suffix = "%b-%d-%Y.txt"
logging.basicConfig(
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[handler, logging.StreamHandler(sys.stdout)])

messages = []

while True:
    user_question = input("User: ")
    if user_question == "exit":
        break
    print("#" * 20)
    messages.append({"role": "user", "content": user_question})
    ai_response = asyncio.run(chat_with_agent(messages, user_question))
    print(f"AI: {ai_response}")
    print("#" * 20)
    messages.append({"role": "assistant", "content": ai_response})