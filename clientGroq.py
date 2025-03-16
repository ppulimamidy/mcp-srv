import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

async def main():
    # Initialize Groq model
    chat_model = ChatGroq(
        model="mixtral-8x7b-32768",  # Groq's Mixtral model
        temperature=0,
        groq_api_key=os.environ.get("GROQ_API_KEY")
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
                    print("\nError with weather service, falling back to Groq")
                    response = await chat_model.ainvoke([HumanMessage(content=user_input)])
                    print("\nAssistant:", response.content)
            else:
                # Use Groq for non-weather queries
                response = await chat_model.ainvoke([HumanMessage(content=user_input)])
                print("\nAssistant:", response.content)

if __name__ == "__main__":
    asyncio.run(main())

