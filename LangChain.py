# Import relevant functionality
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Create the agent
memory = MemorySaver()
config = {"configurable": {"thread_id": "abc123"}}

model = ChatAnthropic(
    model_name="claude-3-7-sonnet-20250219",  # ✅ Use correct model name
    anthropic_api_key="{vars.ANTHROPIC_APIKEY}"
)

search = TavilySearchResults(
    max_results=2,
    tavily_api_key="{vars.TAVILY_APIKEY}")

tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# ✅ Stream (values mode)
for step in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im Sumi! and i live in sf")]},
    config=config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()

# ✅ Stream (values mode for weather)
for step in agent_executor.stream(
    {"messages": [HumanMessage(content="whats the weather where I live?")]},
    config=config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()

# ✅ Stream (messages mode – needs unpacking)
for message, metadata in agent_executor.stream(
    {"messages": [HumanMessage(content="hi!")]},
    config=config,
    stream_mode="messages",
):
    message.pretty_print()
