# Import relevant functionality
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Create the agent
memory = MemorySaver()
model = ChatAnthropic(model_name="claude-3-7-sonnet-20250219", anthropic_api_key="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")
search = TavilySearchResults(max_results=2, tavily_api_key="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")
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for step in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im Sumi! and i live in sf")]},
    config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()

for step in agent_executor.stream(
    {"messages": [HumanMessage(content="whats the weather where I live?")]},
    config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()