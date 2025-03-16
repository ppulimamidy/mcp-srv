import os
from dotenv import load_dotenv
# First we initialize the model we want to use.
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=os.environ.get("OPENAI_API_KEY")
    )

# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal

from langchain_core.tools import tool


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather]


# Define the graph

from langgraph.prebuilt import create_react_agent

graph = create_react_agent(model, tools=tools)

# Option 1: Save the Mermaid graph to a file
with open("graph.mmd", "w") as f:
    f.write(graph.get_graph().draw_mermaid())
print("Mermaid graph saved to graph.mmd")

# Option 2: Print the Mermaid markup directly
print("\nMermaid Graph Markup:")
print(graph.get_graph().draw_mermaid())

# Run the agent
inputs = {"messages": [("user", "what is the weather in sf")]}
for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        print(message.content)