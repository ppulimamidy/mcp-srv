import os
from langchain_openai import ChatOpenAI
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from browser_use import Controller, ActionResult
from typing import List

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class StockPriceResult(BaseModel):
    stock_price: float
    stock_name: str 

class StockPriceResults(BaseModel):  # Moved outside of StockPriceResult
    stock_prices: List['StockPriceResult']    

controller = Controller(output_model=StockPriceResults)

@controller.action
def get_stock_prices(stock_names: List[str]) -> List[StockPriceResult]:
    return [StockPriceResult(stock_price=random.randint(100, 1000), stock_name=stock_name) for stock_name in stock_names]


async def siteValidation():
    task = ('Important: I am a UI Automation tester validating the tasks'
            'Open website http://www.google.com'
            'Click on the search button'
            'Enter the search query "AAPL, TSLA, GOOGL, MSFT, NVDA, AMZN" in the search bar'
            'Click on the search button'
            'Get the stock prices of AAPL, TSLA, GOOGL, MSFT, NVDA, and AMZN'
            'Print the stock prices in a table format'
            )
    agent = Agent(
        task=task,
        # llm=ChatOpenAI(model="gpt-4o"),
        llm=ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Using pro instead of flash
            temperature=0,
            google_api_key=os.environ.get("GEMINI_API_KEY")
        ),
        use_vision=True,
        controller=controller
    )
    history = await agent.run()
    test_result = history.final_result
    print(test_result)

asyncio.run(siteValidation())