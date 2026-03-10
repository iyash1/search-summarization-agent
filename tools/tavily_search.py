import os
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode 

from typing import Literal
from data.models import AgentSearchState
from data.constants import GPT_5_MINI
from dotenv import load_dotenv

load_dotenv()
IS_DEBUG = os.getenv("DEBUG", "False").lower() == "true"

from IPython.display import display, Image

llm = ChatOpenAI(model = GPT_5_MINI, temperature = 0, streaming = True)

tavily_search_tool = TavilySearch(max_results = 3)

# List of tools for this step
tools_list_single = [tavily_search_tool]

# ------------------------------------------------------------------------------------------------------------------------------------------------
# This function creates a node function that binds the provided tools to the language model and calls it with the conversation history (messages).
# ------------------------------------------------------------------------------------------------------------------------------------------------
def make_call_model_with_tools(tools: list):
    def call_model_with_tools(state: AgentSearchState):
        print("DEBUG: Entering call_model_with_tools node") if IS_DEBUG else None
        messages = state["messages"]
        
        # Binds the tools to the language model 
        model_with_tools = llm.bind_tools(tools)

        # Feeds the conversation history (messages) into the model
        response = model_with_tools.invoke(messages)

        # Return the model response as a new message
        return {"messages": [response]}

    return call_model_with_tools

# ------------------------------------------------------------------------------------------------------------------------------------------------
# This function checks the last message in the conversation history to determine whether to continue with tool execution or end the graph.
# ------------------------------------------------------------------------------------------------------------------------------------------------
def should_continue(state: AgentSearchState) -> Literal["action", "__end__"]:
    """Determines the next step: continue with tools or end."""
    print("DEBUG: Entering should_continue node") if IS_DEBUG else None
    last_message = state["messages"][-1]
    
    # Check if the last message is an AIMessage with tool_calls
    if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("DEBUG: Decision: continue (route to action)") if IS_DEBUG else None
        return "action"  # Route to the node named "action"
    else:
        print("DEBUG: Decision: end (route to END)") if IS_DEBUG else None
        return END  # Special value indicating the end of the graph
    
# ------------------------------------------------------------------------------------------------------------------------------------------------
# This function builds a LangGraph with a single tool integrated into the workflow. 
# It defines the nodes, edges, and the logic for when to call the tool versus when to end the graph.
# ------------------------------------------------------------------------------------------------------------------------------------------------
def build_graph_one_tool(tools_list):

    # Let's Instantiate ToolNode
    tool_node = ToolNode(tools_list)

    # Define the call_node_fn, which binds the tools to the LLM and calls OpenAI API
    call_node_fn = make_call_model_with_tools(tools_list)       

    # Build the Graph with One Tool using ToolNode
    graph_one_tool = StateGraph(AgentSearchState)

    # Add nodes
    graph_one_tool.add_node("agent", call_node_fn)
    
    # Add the ToolNode instance directly, naming it "action"
    graph_one_tool.add_node("action", tool_node)

    # Set entry point
    graph_one_tool.set_entry_point("agent")

    # Add a conditional edge from the agent
    # The dictionary maps the return value of 'should_continue' ("action" or END)
    # to the name of the next node ("action" or the special END value).
    graph_one_tool.add_conditional_edges(
        "agent",  # Source node name
        should_continue,  # Function to decide the route
        {"action": "action", END: END},  # Mapping: {"decision": "destination_node_name"}
    )

    # Add edge from action (ToolNode) back to agent
    graph_one_tool.add_edge("action", "agent")

    # Compile the graph
    app = graph_one_tool.compile()

    # Visualize
    display(Image(app.get_graph().draw_mermaid_png()))

    return app

# ------------------------------------------------------------------------------------------------------------------------------------------------
# This function serves as a wrapper to call the LangGraph app with a given input message. 
# It initializes the conversation state, invokes the graph, and processes the final output.
# ------------------------------------------------------------------------------------------------------------------------------------------------
def app_call(app, messages):
    # Initialize the state with the provided messages
    initial_state = {"messages": [HumanMessage(content=messages)]}

    # Invoke the app with the initial state
    final_state = app.invoke(initial_state)

    # Iterate through the messages in the final state
    if IS_DEBUG:
        for i in final_state["messages"]:
            # Print the type of the message in markdown format
            print(i.type)
            # Print the content of the message in markdown format
            print(i.content)
            # Print any additional kwargs associated with the message
            if i.additional_kwargs != {}:
                print(i.additional_kwargs)

    # Return the content of the last message and the final state
    return final_state["messages"][-1].content, final_state

# ------------------------------------------------------------------------
# Build the graph with the single tool and run a test message through it
# ------------------------------------------------------------------------
def search_graph_tool(input_message: str):
    app = build_graph_one_tool(tools_list_single)

    # messages = "What's the latest news on France in May 2025? Is it a good time to visit?"
    output, history = app_call(app, input_message)

    print("\n==================== OUTPUT ====================")
    print(output)

    if IS_DEBUG:
        print("\n==================== HISTORY ===================")
        print(history)