import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

async def main():
    # Initialize OpenAI model
    chat_model = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    async with MultiServerMCPClient(
        {
            "weather": {
                "url": "http://0.0.0.0:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        tools = client.get_tools()
        weather_tool = tools[0]  # Get the weather tool
        
        print("Chat started (type 'quit' to exit)")
        print("Ask me about weather or anything else!")
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == 'quit':
                break
            
            if "weather" in user_input.lower():
                # Use weather service
                try:
                    response = await weather_tool.ainvoke({"location": user_input})
                    print("\nWeather Service:", response)
                except Exception as e:
                    print("\nError with weather service, falling back to OpenAI")
                    response = await chat_model.ainvoke([HumanMessage(content=user_input)])
                    print("\nAssistant:", response.content)
            else:
                # Use OpenAI for non-weather queries
                response = await chat_model.ainvoke([HumanMessage(content=user_input)])
                print("\nAssistant:", response.content)

if __name__ == "__main__":
    asyncio.run(main())