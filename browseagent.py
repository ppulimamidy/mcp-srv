import os
from langchain_openai import ChatOpenAI
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

async def main():
    agent = Agent(
        task="get the stock prices of AAPL, TSLA, GOOGL, MSFT, NVDA, and AMZN",
        # llm=ChatOpenAI(model="gpt-4o"),
        llm=ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Using pro instead of flash
            temperature=0,
            google_api_key=os.environ.get("GEMINI_API_KEY")
        ),
    )
    await agent.run()

asyncio.run(main())