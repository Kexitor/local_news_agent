"""
Usage Sample for Local News Agent

This file demonstrates how to interact with the local news agent in an interactive CLI environment.
It shows a complete example of:
- Setting up logging
- Managing conversation history
- Calling the news agent with user input
- Processing and displaying responses

The sample creates a simple chat interface where users can ask questions about news,
and the agent will respond based on current news content from the configured source.
"""

from logging.handlers import TimedRotatingFileHandler
import sys
import logging
from news_agent import chat_with_agent
import asyncio
import os
import config

# Ensure logs directory exists
os.makedirs(config.logs_path, exist_ok=True)

# Setup logging with rotating file handler and console output
handler = TimedRotatingFileHandler(config.logs_path + "logs.txt", when="midnight", backupCount=2)
handler.suffix = "%b-%d-%Y.txt"
logging.basicConfig(
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[handler, logging.StreamHandler(sys.stdout)])

# Initialize conversation history list
messages = []

# Main interactive loop
while True:
    # Get user input
    user_question = input("User: ")
    
    # Exit condition
    if user_question == "exit":
        break
    
    # Display separator for better readability
    print("#" * 20)
    
    # Add user message to conversation history

    # Process the user question through the news agent with conversation history
    ai_response = asyncio.run(chat_with_agent(messages, user_question))
    messages.append({"role": "user", "content": user_question})
    
    # Display AI response
    print(f"AI: {ai_response}")
    
    # Display separator for better readability
    print("#" * 20)
    
    # Add AI response to conversation history
    messages.append({"role": "assistant", "content": ai_response})
