import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

async def main():
    # Initialize the model
    model = genai.GenerativeModel('gemini-2.0-flash')
    chat = model.start_chat()

    # Connect to MCP server
    async with MultiServerMCPClient(
        {
            "weather": {
                "url": "http://0.0.0.0:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        tools = client.get_tools()
        weather_tool = tools[0]  # Get the first tool (weather)
        
        print("Chat started (type 'quit' to exit)")
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == 'quit':
                break

            if "weather" in user_input.lower():
                # Use MCP server for weather queries
                response = await weather_tool.ainvoke({"location": user_input})
                print("\nWeather Service:", response)
            else:
                # Use Gemini for other queries
                response = chat.send_message(user_input)
                print("\nGemini:", response.text)

                # Define the graph


if __name__ == "__main__":
    asyncio.run(main())
    